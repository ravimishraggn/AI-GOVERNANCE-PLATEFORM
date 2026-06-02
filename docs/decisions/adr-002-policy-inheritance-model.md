# ADR-002: Policy Inheritance Model

**Status:** Accepted
**Date:** 2026-05-31

## Decision

Implement a strict hierarchical policy inheritance model where child policies can only
add restrictions, never remove them. Resolution rule: more restrictive always wins.

## Rationale

Alternative approaches considered:
1. **Flat policy model**: All policies at the same level, conflicts resolved explicitly.
   Rejected: does not scale to 100+ teams with different requirements.

2. **Override-friendly model**: Children can override parents with sufficient authority.
   Rejected: creates a governance loophole. A sufficiently authorized team lead could
   effectively disable platform-level safety controls.

3. **Additive-only model (chosen)**: Children can only add restrictions.
   Accepted: preserves platform-level baseline while enabling tenant and team customization.

## Key Implication

A platform policy that requires prompt injection detection ENABLED cannot be disabled by
any tenant or team configuration. This is intentional and is communicated clearly in the
developer documentation. Teams that need exceptions must go through the formal exception
process with time-bounded grants.
