# Frozen register-dispatch v1 projection

This directory freezes the exact register-dispatch files from commit `b3bc638` (the parent of
`f981397`) under their installation-relative paths. Its colocated v1 manifest pins those frozen
bytes and is the source used by `-LegacyVerification -Check`.

The older root `implementations/contracts/register-dispatch-runtime-package.v1.json` remains
byte-unchanged. Three of its declared hashes do not match the recoverable predecessor bytes, so it
is retained as historical evidence but is not represented as a working verification package. This
projection does not claim to reconstruct those unavailable bytes; it makes the last recoverable
v0.6.4 file set independently and repeatably verifiable.
