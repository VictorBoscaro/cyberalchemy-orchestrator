# Canonicalization — RWO-CVG-001

Status: `design-only; planned and unexecuted`
Profile: `rwo-convergence-cjson/v1`

## Canonical JSON

Canonical documents are UTF-8 JSON followed by exactly one LF. Duplicate keys,
floats, non-finite numbers, integers outside the I-JSON safe range, non-ASCII
object keys, lone surrogates, non-NFC strings, and unknown schema fields are
rejected. Object keys sort by ascending ASCII byte sequence. Arrays retain
declared order. Strings use JSON short escapes for quote, reverse solidus,
backspace, tab, LF, form feed and carriage return; other U+0000–U+001F controls
use lowercase `\u00xx`; all other scalar values are emitted as UTF-8 without
ASCII escaping. The separators are `,` and `:` with no surrounding whitespace.
SHA-256 covers the complete bytes including the final LF.

A validator parses the file with duplicate-key detection, re-emits it using
this profile, and requires byte equality. Two clean builds from the same bound
inputs must produce identical bytes.

## Tree digest

Final package paths are repository-independent relative UTF-8 paths. Symlinks,
absolute paths, parent traversal and duplicate normalized paths are forbidden.
Sort paths by raw UTF-8 bytes. For each regular file append this framing:

```text
path_utf8 NUL decimal_size_ascii NUL lowercase_sha256_ascii LF
```

The tree digest is SHA-256 over the concatenation of those records. File modes
are validated against the schema but are not silently normalized; any allowed
mode is recorded in the separate manifest and therefore validated before the
tree digest is accepted.

## Runner evidence classes

An `exit-only` runner may contribute only descriptor identity, executable and
snapshot bindings, attempt/termination facts and its narrow check status. It
cannot derive fixture IDs or skip facts from console prose.

A `structured-evidence` runner writes one declared schema-validated file. Its
receipt binds the raw evidence path, byte length, SHA-256, schema version and
normalizer path/version/SHA-256. The normalizer output is canonical JSON under
this profile. If any claim-critical fact is parsed from stdout or stderr, the
complete raw byte stream, length and normalizer binding become canonical
inputs; otherwise console output remains non-canonical diagnostics and cannot
support a claim.
