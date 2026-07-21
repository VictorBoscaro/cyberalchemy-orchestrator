You are seat `seat-a` in round `round-1` of a sealed collection.

Complete the assigned analysis independently. You must publish the official contribution exactly
once through the `bus_publish` tool before finishing. Use:

- `operation_id`: `operation-a-1`
- `round_id`: `round-1`
- `message_type`: `position`
- `idempotency_key`: `position:seat-a:round-1`
- `payload`: a JSON object containing your full contribution

Do not attempt to read another seat's contribution. After publication, return only this JSON shape:

```json
{
  "publication_receipt": {
    "receipt_version": 1,
    "status": "accepted",
    "event_id": "...",
    "message_id": "...",
    "journal_offset": 1,
    "payload_hash": "sha256:...",
    "idempotency_key": "position:seat-a:round-1",
    "replayed": false
  }
}
```

Copy the receipt values exactly from the successful tool response. If the tool is unavailable or
rejects the publication, report the failure; do not present an unpublished contribution as official.
