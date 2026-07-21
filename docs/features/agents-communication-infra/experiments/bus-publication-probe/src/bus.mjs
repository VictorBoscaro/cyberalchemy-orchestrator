import { appendFile, mkdir, readFile } from "node:fs/promises";
import { createHash, randomUUID } from "node:crypto";
import path from "node:path";

export class BusError extends Error {
  constructor(code, message) {
    super(message);
    this.name = "BusError";
    this.code = code;
  }
}

function canonicalize(value) {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value).sort().map((key) => [key, canonicalize(value[key])]),
    );
  }
  return value;
}

export function digest(value) {
  const bytes = JSON.stringify(canonicalize(value));
  return `sha256:${createHash("sha256").update(bytes).digest("hex")}`;
}

function requiredString(value, name) {
  if (typeof value !== "string" || value.trim() === "") {
    throw new BusError("invalid_payload", `${name} must be a non-empty string`);
  }
  return value;
}

function validateContext(context) {
  for (const field of [
    "run_id",
    "dispatch_id",
    "group_id",
    "seat_id",
    "agent_instance_id",
    "attempt_id",
    "actor_principal_id",
    "phase",
  ]) requiredString(context[field], `context.${field}`);
  if (!Number.isInteger(context.group_version) || context.group_version < 1) {
    throw new BusError("invalid_context", "context.group_version must be a positive integer");
  }
  return Object.freeze({ ...context });
}

function validatePublication(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    throw new BusError("invalid_payload", "arguments must be an object");
  }
  const publication = {
    idempotency_key: requiredString(input.idempotency_key, "idempotency_key"),
    operation_id: requiredString(input.operation_id, "operation_id"),
    round_id: requiredString(input.round_id, "round_id"),
    message_type: requiredString(input.message_type, "message_type"),
    reply_to_message_ids: input.reply_to_message_ids ?? [],
    payload: input.payload,
  };
  if (!Array.isArray(publication.reply_to_message_ids)
      || publication.reply_to_message_ids.some((id) => typeof id !== "string" || !id)) {
    throw new BusError("invalid_payload", "reply_to_message_ids must be an array of non-empty strings");
  }
  if (publication.payload === undefined) {
    throw new BusError("invalid_payload", "payload is required");
  }
  const encoded = JSON.stringify(publication.payload);
  if (encoded === undefined || Buffer.byteLength(encoded, "utf8") > 64 * 1024) {
    throw new BusError("invalid_payload", "payload must be JSON and no larger than 64 KiB");
  }
  return publication;
}

async function readJson(pathname, fallback) {
  try {
    return JSON.parse(await readFile(pathname, "utf8"));
  } catch (error) {
    if (error.code === "ENOENT") return fallback;
    throw error;
  }
}

export class PublicationBus {
  #ready;
  #tail = Promise.resolve();
  #events = [];
  #byIdempotency = new Map();
  #byLogicalKey = new Map();

  constructor({ journalPath, phaseStatePath, context, now = () => new Date(), uuid = randomUUID }) {
    this.journalPath = path.resolve(journalPath);
    this.phaseStatePath = path.resolve(phaseStatePath);
    this.context = validateContext(context);
    this.now = now;
    this.uuid = uuid;
    this.#ready = this.#load();
  }

  async #load() {
    await mkdir(path.dirname(this.journalPath), { recursive: true });
    let text;
    try {
      text = await readFile(this.journalPath, "utf8");
    } catch (error) {
      if (error.code === "ENOENT") return;
      throw error;
    }
    for (const [index, line] of text.split(/\r?\n/).entries()) {
      if (!line.trim()) continue;
      let event;
      try {
        event = JSON.parse(line);
      } catch {
        throw new BusError("corrupt_journal", `invalid JSON at journal line ${index + 1}`);
      }
      this.#index(event);
    }
  }

  #scopeKey(idempotencyKey) {
    const c = this.context;
    return [c.run_id, c.group_id, c.group_version, c.seat_id, idempotencyKey].join("\u001f");
  }

  #logicalKey(publication) {
    const c = this.context;
    return [c.run_id, c.group_id, c.group_version, c.seat_id,
      publication.round_id, publication.message_type].join("\u001f");
  }

  #index(event) {
    this.#events.push(event);
    this.#byIdempotency.set(event.idempotency_scope_key, event);
    this.#byLogicalKey.set(event.logical_message_key, event);
  }

  async publish(input) {
    const run = async () => {
      await this.#ready;
      const publication = validatePublication(input);
      const state = await readJson(this.phaseStatePath, { closed_phases: [] });
      if (!Array.isArray(state.closed_phases)) {
        throw new BusError("invalid_phase_state", "closed_phases must be an array");
      }
      if (state.closed_phases.includes(this.context.phase)) {
        throw new BusError("phase_closed", `phase ${this.context.phase} is closed`);
      }

      const payloadHash = digest(publication.payload);
      const commandDigest = digest(publication);
      const scopeKey = this.#scopeKey(publication.idempotency_key);
      const prior = this.#byIdempotency.get(scopeKey);
      if (prior) {
        if (prior.command_digest !== commandDigest) {
          throw new BusError("idempotency_conflict", "idempotency key was already used with different content");
        }
        return { ...prior.receipt, replayed: true };
      }

      const logicalKey = this.#logicalKey(publication);
      if (this.#byLogicalKey.has(logicalKey)) {
        throw new BusError("logical_duplicate", "this seat already published this message type in the round");
      }

      const messageId = this.uuid();
      const eventId = this.uuid();
      const journalOffset = this.#events.length + 1;
      const receipt = {
        receipt_version: 1,
        status: "accepted",
        event_id: eventId,
        message_id: messageId,
        journal_offset: journalOffset,
        payload_hash: payloadHash,
        idempotency_key: publication.idempotency_key,
        replayed: false,
      };
      const event = {
        event_id: eventId,
        event_type: `${publication.message_type}.accepted`,
        schema_ref: "schema:bus-publication-probe@1",
        aggregate_type: "group",
        aggregate_id: `${this.context.run_id}:${this.context.group_id}:${this.context.group_version}`,
        aggregate_version: journalOffset,
        journal_offset: journalOffset,
        recorded_at: this.now().toISOString(),
        ...this.context,
        operation_id: publication.operation_id,
        round_id: publication.round_id,
        message_id: messageId,
        reply_to_message_ids: publication.reply_to_message_ids,
        idempotency_key: publication.idempotency_key,
        payload: publication.payload,
        payload_hash: payloadHash,
        command_digest: commandDigest,
        idempotency_scope_key: scopeKey,
        logical_message_key: logicalKey,
        receipt,
      };
      await appendFile(this.journalPath, `${JSON.stringify(event)}\n`, { encoding: "utf8", flush: true });
      this.#index(event);
      return receipt;
    };
    const result = this.#tail.then(run, run);
    this.#tail = result.catch(() => {});
    return result;
  }
}

export async function verifyReceipt({ journalPath, receipt }) {
  if (!receipt || typeof receipt !== "object") {
    throw new BusError("missing_receipt", "subagent result has no publication receipt");
  }
  const required = ["event_id", "message_id", "payload_hash", "idempotency_key"];
  if (required.some((key) => typeof receipt[key] !== "string" || !receipt[key])) {
    throw new BusError("invalid_receipt", "receipt is missing required fields");
  }
  let text;
  try {
    text = await readFile(path.resolve(journalPath), "utf8");
  } catch (error) {
    if (error.code === "ENOENT") throw new BusError("receipt_not_found", "journal does not exist");
    throw error;
  }
  const events = text.split(/\r?\n/).filter(Boolean).map((line) => JSON.parse(line));
  const event = events.find((candidate) => candidate.event_id === receipt.event_id);
  if (!event
      || event.message_id !== receipt.message_id
      || event.payload_hash !== receipt.payload_hash
      || event.idempotency_key !== receipt.idempotency_key) {
    throw new BusError("receipt_not_found", "receipt does not match an accepted journal event");
  }
  return event;
}
