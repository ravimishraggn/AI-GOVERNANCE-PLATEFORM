# ADR-001: Immutable Append-Only Audit Log

**Status:** Accepted
**Date:** 2026-05-31
**Deciders:** Platform Architect, Security Architect, Compliance Lead

## Context

The Governance Platform must record every significant governance event in a way that
satisfies regulatory evidence requirements (SEC Rule 17a-4, SR 11-7) and supports
forensic investigation. The key question: how do we ensure audit records cannot be
tampered with, even by platform administrators?

## Decision

Implement the audit log as an append-only, cryptographically chained event store:

1. **Append-only storage**: No UPDATE or DELETE operations are permitted on audit records.
   The storage engine enforces this at the infrastructure level (S3 Object Lock, or
   equivalent), not just at the application level.

2. **Cryptographic chaining**: Each audit event contains the SHA-256 hash of the
   previous event. Any modification to any past event breaks the chain, making tampering
   detectable by running `VerifyIntegrity`.

3. **HSM-backed signing**: Each event is digitally signed by the Governance Platform's
   signing key, stored in a Hardware Security Module. The private key never leaves the HSM.

4. **Separation of administration**: The audit store is administered by the Governance
   Team using separate IAM credentials from all other platform services. Application
   teams and infrastructure teams cannot access the audit store directly.

5. **Periodic anchoring**: Merkle tree roots are published to an external immutable log
   at regular intervals, providing a third-party witness to the chain state.

## Consequences

**Positive:**
- Audit records are tamper-evident by construction, not by policy
- Regulatory evidence is credible for examination purposes
- Chain verification can be run on demand and reported to compliance
- No "admin backdoor" that could compromise audit integrity

**Negative:**
- Storage costs are higher (no deletion or compaction)
- Correcting an incorrect audit record requires a correction event (new append), not a fix
- The signing key rotation process requires careful ceremony to maintain chain validity

## Alternatives Considered

**Encrypted audit database with access controls:** Rejected. Access controls are policy
controls, not technical controls. A sufficiently privileged attacker or accidental
configuration change could modify records. Not acceptable for regulatory evidence.

**Third-party audit SaaS:** Evaluated. Introducing a third-party SaaS for audit creates
data sovereignty risks, vendor lock-in for regulatory-critical infrastructure, and
contractual complexity for regulated tenants. Not recommended for Phase 1-2. May be
reconsidered for Phase 4 ecosystem integrations.
