# RWO Rust semantic-core prototype

This crate is an offline Rust implementation of the RWO raw-admission and pure
semantic core. It reads the frozen 54-vector conformance manifest as an
expectation corpus and covers raw UTF-8 JSON admission, compile, reduce,
command-intent, defect ordering, normalization, typed digests, version tuples,
retry classification, and read-only fixture-integrity checks.

Raw admission is host-pinned for this candidate-local prototype: the only
localized `unsafe` code binds Linux `libicuuc.so.74` symbols and fails vector
validation unless the runtime reports Unicode `15.1.0`. ICU supplies assigned
scalar classification and NFC checks; the crate's own parser preserves duplicate
decoded object names and numeric token lexemes before converting to JSON values.
This is intentionally not a portable bundled-Unicode distribution yet.

## Non-goals

This crate does not implement or claim:

- a journal, accepted-history owner, queue, transport, gRPC service, or adapter;
- command delivery, retry scheduling, waiting, backoff, leases, or dead letters;
- work execution, effects, compensation, credentials, policy, ACI, ARE, or
  inference; or
- cross-language source binding, source-bound release, production readiness,
  or ownership/promotion authority; or
- a portable runtime for hosts without the pinned ICU 74 / Unicode 15.1 ABI.

`classify_retry` is a pure classification function only. `RetrySame` preserves
semantic identity in its returned classification; it never performs a retry.

## Validation

From the repository root:

```bash
cargo test --manifest-path implementations/rwo-rust/Cargo.toml --offline
```

The tests load the existing frozen manifest at test time and never regenerate or
rewrite its expectations. `rwo_fixture_observations` emits a canonical offline
observation document that the Python oracle compares independently.
