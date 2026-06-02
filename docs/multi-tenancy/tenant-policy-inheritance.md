# Tenant Policy Inheritance Model

## The Inheritance Hierarchy

```
Platform Policy Layer (IMMUTABLE BASELINE)
│
│ Platform-wide policies ALL tenants MUST satisfy.
│ No tenant can override, weaken, or disable these.
│ Examples:
│   - PII handling requirements
│   - Prompt injection detection (mandatory for all agents)
│   - Data exfiltration prevention
│   - Model abuse monitoring
│   - Audit logging requirements
│
├── Regulatory Policy Layer (JURISDICTION-SPECIFIC)
│   │
│   │ Policies derived from regulations applicable to the tenant's
│   │ jurisdiction and regulatory profile.
│   │ Tenants in EU inherit GDPR policies.
│   │ SEC-registered advisers inherit SR 11-7 model risk policies.
│   │ Cannot be overridden by tenant; applied automatically by profile.
│   │
│   ├── Tenant Policy Layer (TENANT-CONFIGURABLE)
│   │   │
│   │   │ Tenant-specific policies that EXTEND the platform and regulatory
│   │   │ baseline. A tenant CAN be MORE restrictive but NEVER less.
│   │   │ Examples:
│   │   │   - Restrict to specific approved model providers
│   │   │   - Stricter data retention requirements
│   │   │   - Custom approval workflows
│   │   │   - Firm-specific ethical guidelines
│   │   │
│   │   ├── Team Policy Layer (TEAM-CONFIGURABLE)
│   │   │   │
│   │   │   │ Team-specific policies within a tenant.
│   │   │   │ Teams can further restrict; they cannot loosen tenant policies.
│   │   │   │ Examples:
│   │   │   │   - Cost budget limits per team
│   │   │   │   - Team-specific model restrictions
│   │   │   │
│   │   │   └── Application Policy Layer (APPLICATION-SPECIFIC)
│   │   │
│   │   │       Application-level configuration within all parent bounds.
│   │   │       Cannot override any parent policy.
```

---

## The Golden Rule

> A child policy can only ADD restrictions, never REMOVE them.
> The child must satisfy the parent plus its own constraints.
> The effective policy for any artifact is the intersection of all parent constraints.

---

## Policy Composition Example

Scenario: Tenant B's Team X deploys Agent Y using Model Z on data classified as Restricted.

```
Step 1: Resolve Platform Policies applicable to Agent with Restricted data
  → PlatformPolicy-001: PII handling required
  → PlatformPolicy-002: Audit level DETAILED required
  → PlatformPolicy-003: Prompt injection detection ENABLED required

Step 2: Resolve Regulatory Policies for Tenant B (US, SEC-registered)
  → SEC-AI-001: Human review required for investment recommendations
  → SR11-7-001: Model documentation required
  → SEC-17a4-001: Execution records retained 7 years

Step 3: Resolve Tenant B Custom Policies
  → TenantB-001: Model providers restricted to [anthropic, openai] only
  → TenantB-002: No provider data retention beyond 90 days
  → TenantB-003: MNPI-classified data requires dedicated namespace

Step 4: Resolve Team X Policies
  → TeamX-001: Max context window 32k tokens for cost control
  → TeamX-002: Max cost per execution $0.50

Step 5: Effective Policy for Agent Y
  MUST: PII handling, DETAILED audit, injection detection
  MUST: Human review before investment outputs, model docs, 7-year retention
  RESTRICTED TO: anthropic, openai providers
  MUST NOT: Use provider with >90 day data retention
  MUST: Dedicated namespace if MNPI data touched
  MAXIMUM: 32k context window, $0.50 per execution
```

---

## Override Mechanism

Overrides are time-bounded exceptions to the inheritance hierarchy:

```yaml
PolicyOverride:
  override_id: UUID
  policy_id: PolicyRef
  artifact_id: ArtifactRef          # scope: specific artifact only
  granted_by: PersonRef             # must have override_permission for this policy
  granted_at: datetime
  expires_at: datetime              # MANDATORY — no perpetual overrides
  rationale: string                 # recorded in immutable audit log
  conditions: string                # conditions on the override

# Every policy evaluation that uses an override is flagged in the audit record.
# Overrides approaching expiry trigger renewal workflows.
# Expired overrides are automatically revoked — no manual action required.
```

---

## Conflict Resolution Algorithm

```python
# When multiple applicable policies have conflicting requirements:

def resolve_conflict(policies: List[Policy], artifact: Artifact) -> PolicyDecision:
    # 1. Platform policies always win
    platform_constraints = extract_constraints(filter_by_scope(policies, PLATFORM))

    # 2. Among same-scope policies, more restrictive wins
    all_constraints = merge_most_restrictive(policies)

    # 3. Explicit prohibitions override explicit permissions
    if any_prohibition(all_constraints, artifact):
        return DENY

    # 4. Unresolvable conflicts: flag for human, apply most restrictive
    if has_irresolvable_conflict(all_constraints):
        flag_for_human_resolution()
        return DENY  # most restrictive pending resolution

    return evaluate(all_constraints, artifact)
```
