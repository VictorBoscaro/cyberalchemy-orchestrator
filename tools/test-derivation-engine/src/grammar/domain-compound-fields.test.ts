import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import { parse } from "./index.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ACI_SPECS = resolve(
  __dirname,
  "../../../../docs/features/agents-communication-infra/specs",
);

describe("domain compound field declarations", () => {
  it("emits one declaration per code-spanned field identifier", () => {
    const { graph } = parse(ACI_SPECS);
    const fields = graph.nodes
      .filter(
        (node) =>
          node.type === "DomainField" &&
          node.fields.entity === "PublicationCandidate",
      )
      .map((node) => String(node.fields.field));

    expect(fields).toEqual(
      expect.arrayContaining([
        "group_aggregate_id",
        "attempt_id",
        "operation_id",
        "seat_id",
        "round_id",
        "message_type",
      ]),
    );
    expect(fields.some((field) => field.includes("`, `"))).toBe(false);
  });
});
