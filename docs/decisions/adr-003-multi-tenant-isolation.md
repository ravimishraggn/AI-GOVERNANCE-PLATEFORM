# ADR-003: Multi-Tenant Isolation Strategy

**Status:** Accepted
**Date:** 2026-05-31

## Decision

Implement three isolation tiers (Logical, Namespace, Dedicated) rather than a single
uniform isolation approach.

## Rationale

A single isolation model forces a choice between expensive (dedicated infra for all) and
inadequate (shared infra for all). The tiered model matches isolation cost to risk:

- Internal teams and small customers: Logical isolation is sufficient and cost-effective
- Regulated customers with MNPI or data sovereignty requirements: Namespace isolation
- Large institutional investors with their own regulatory obligations: Dedicated isolation

The key technical decision is to implement tenant-specific encryption keys from day one,
even for Tier 1 logical isolation. This means: even if the logical isolation were somehow
bypassed, Tenant A's data encrypted with Tenant A's keys cannot be read without those keys.
Encryption provides defense-in-depth beyond access control.

## Consequences

- Key management complexity increases with number of tenants
- Key rotation ceremonies required per tenant
- Dedicated tier requires separate deployment automation

## Migration Path

A tenant can move from Logical → Namespace → Dedicated without data migration, because
the encryption key model is tenant-specific from the start. The migration changes where
the physical data is stored, not the logical model.
