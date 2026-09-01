# RWO Go gRPC sidecar boundary

This package is a candidate-local boundary around the RWO Rust kernel. Rust
remains the only compiler/reducer and semantic command owner. The Go host now
adds one Linux-local durable log, physical attempt/fence state, a
content-addressed seat-material resolver, an exact tool-free Eve-shaped leaf,
and terminal convergence back through Rust. It does not contain ARE reasoning
or a second semantic scheduler.

The input envelope keeps two kinds of data separate:

- the exact raw bytes of an already accepted event plus its semantic version
  tuple; and
- transport-only delivery metadata such as adapter name and physical attempt
  ID.

Only the former reaches `Kernel.Reduce`. The latter is returned as an
observation and never participates in RWO semantic identity.

`NewGRPCServer` and `NewGRPCClient` expose one local unary route:
`/rwo.v1.EventBoundary/Reduce`. The route uses a handwritten service descriptor
and an explicit `rwo-json` codec because this prototype has no generated
protobuf schema. `[]byte` fields use JSON base64 encoding, keeping the nested
accepted-event payload opaque and byte-exact across the gRPC boundary.

`grpc_test.go` uses gRPC-Go's in-memory `bufconn` transport to prove that a
real RPC preserves raw event bytes, excludes delivery metadata from
`KernelRequest`, and turns one kernel uncertainty into one `unknown`
observation without inventing a retry. It is local HTTP/2 evidence only: it is
not TCP/TLS deployment, protobuf-generation, remote-service, or
arbitrary-adapter-interchangeability evidence.

The durable candidate uses an exclusive Linux `flock` and a checksummed,
append-only `runtime.rwolog`. A record is acknowledged only after a complete
write and file `Sync`; uncertainty poisons the live descriptor until a verified
reopen. Recovery truncates only an incomplete final frame and rejects complete
corruption. This proves the tested host/filesystem behavior, not multi-host
coordination or protection against hardware that lies about `fsync`.

`AttemptCoordinator` distinguishes semantic command identity, physical attempt
identity, and send-try identity. It persists `send_armed` before an Eve create,
freezes ambiguous delivery, permits another try only after exact not-sent
evidence, and maps a late session only through exact lineage. It never creates
a semantic retry. Preparation requires the command identity to exist in a
verified `SemanticCommitV1` outbox record, every transition appends against the
same store-tip snapshot from which it was derived, and acknowledgement requires
an exact persisted terminal-admission marker plus its Rust no-successor semantic
commit. Caller-provided success prose is insufficient.

The first leaf is deliberately fake-Eve-only. `SeatMaterialCatalog` binds one
closed manifest and output schema under an allowed root. `EveLeafAdapter`
accepts numeric loopback URLs only, sends one closed task request, and persists
the exact LF-bearing NDJSON lines before interpretation. The terminal validator
accepts only `session.started`, `task.output`, and `session.completed`, rejects
tools/delegation/workflows/governance-shaped output, converges equivalent
provider representations, and submits the canonical terminal event through
the durable Rust runtime.

Known semantic residue: the selected address form
`seatv1:sha256:<hex>` works in the current Rust implementation, whose fixture
payload check accepts a nonempty `job_id`, but it does not match the frozen
inline registry regex. This prototype therefore proves current implementation
behavior, not formal conformance of that colon-form address to the published
inline payload schema.

`NewHTTPHandler` remains a local reference adapter. Future socket, Redis,
cloud-bus, or in-memory adapters must implement the same
`IngressAdapter` / `CommandAdapter` boundary and prove equivalent invariants.

The pinned `google.golang.org/grpc v1.83.0` dependency requires Go 1.25 or
newer. The current candidate-local runner uses Go 1.25.12.

Build the Rust child and run the complete local validation:

```bash
cargo build --offline --manifest-path ../rwo-rust/Cargo.toml --bin rwo_kernel_child
RWO_KERNEL_CHILD=../rwo-rust/target/debug/rwo_kernel_child \
  GOTOOLCHAIN=go1.25.12 GOFLAGS=-count=1 go test -race ./...

RWO_KERNEL_CHILD=../rwo-rust/target/debug/rwo_kernel_child \
  GOTOOLCHAIN=go1.25.12 GOFLAGS=-count=1 \
  go test -race -run '^TestDurableFailureMatrix$' -v ./...
```

The loopback gRPC host requires every binding explicitly:

```bash
go run ./cmd/rwo-local-runtime \
  --composition testdata/eve-one-seat/composition.json \
  --composition-tuple testdata/eve-one-seat/composition-tuple.json \
  --registry ../../docs/features/recursive-work-orchestrator/development/decision-gates/20260807T173437Z-rwo-language-contract-v2/schemas/registry.json \
  --kernel-child ../rwo-rust/target/debug/rwo_kernel_child \
  --store /tmp/rwo-local/runtime.rwolog \
  --store-instance-id local-example-1 \
  --material-root testdata/eve-one-seat \
  --listen 127.0.0.1:0
```

The command has no Eve endpoint and performs no external delivery. Real Eve
compatibility, credentials, durable provider reconciliation, production data
retention, multi-seat/multi-host operation, lifecycle synchronization,
publication, deployment, and production readiness remain outside this proof.
