# Audit Service

## Purpose

The Audit Service maintains the immutable, cryptographically tamper-evident record of
every significant governance event. It is the court of record for the enterprise's AI
governance and the primary evidence source for regulatory examinations.

## Design Principles

1. **Write path is fire-and-forget**: Recording an audit event must never block the
   calling service. Audit writes are asynchronous and acknowledged immediately.

2. **Immutability is enforced at the storage layer**: Audit records are stored in
   append-only object storage with Object Lock enabled. The application layer cannot
   delete or modify records.

3. **Cryptographic chaining**: Each event contains the SHA-256 hash of the prior event,
   making any tampering detectable by running VerifyIntegrity.

4. **Query path is separate from write path**: High-throughput writes go to a streaming
   buffer; reads go to an indexed query engine. These are separate services.

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/events` | Record an audit event (async) |
| GET | `/v1/events/{event_id}` | Get a specific event |
| POST | `/v1/trails/query` | Query audit trail by criteria |
| GET | `/v1/trails/{artifact_id}` | Get full audit trail for an artifact |
| POST | `/v1/trails/{artifact_id}/reconstruct` | Reconstruct state at a timestamp |
| POST | `/v1/trails/verify` | Verify integrity of an audit trail |
| POST | `/v1/reports/generate` | Generate formatted audit report |
| POST | `/v1/evidence/export` | Export evidence package (compliance use) |

## Retention

Retention policies are configured per event class. The audit service enforces retention
automatically. Events cannot be deleted before their retention period expires.

See [docs/control-planes/audit-plane.md](../../../docs/control-planes/audit-plane.md)
for the full retention policy table.

## Performance Requirements

| Operation | SLA |
|-----------|-----|
| Write event | < 5ms (ack only; actual write is async) |
| Query trail (7-day window) | P99 < 2s |
| Reconstruct state | P99 < 5s |
| Generate report | Async, < 5 minutes |
