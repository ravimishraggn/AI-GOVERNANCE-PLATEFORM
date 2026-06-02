# Agent Metadata Model

## Why Agent Metadata Matters

An agent without governance metadata is ungovernable. You cannot evaluate risk, apply
policies, produce audit trails, or satisfy regulatory requirements for an agent that has
not declared what it is, what it does, who owns it, and what it touches.

Agent metadata is the governance contract between the product team and the platform.

---

## Complete Schema

```yaml
AgentRecord:
  # ── Identity ──────────────────────────────────────────────────
  agent_id: UUID                    # platform-assigned, immutable
  canonical_name: string            # stable identifier: org.team.agent-name
  display_name: string              # human-readable
  version: semver                   # semantic version of this agent configuration
  description: string               # what this agent does, for whom, and why

  # ── Ownership ─────────────────────────────────────────────────
  owning_team: TeamRef
  owning_tenant: TenantRef
  business_owner:                   # accountable for what the agent does
    person_id: PersonRef
    name: string
    email: string
  technical_owner:                  # accountable for how the agent works
    person_id: PersonRef
    name: string
    email: string

  # ── Classification ────────────────────────────────────────────
  agent_type: enum[Conversational, TaskExecution, Research,
                   Orchestration, Monitoring, Valuation, Analysis]
  use_case: string                  # business use case description
  target_users: string[]            # Investment Analysts, Portfolio Managers, etc.
  autonomy_level: enum[HumanInLoop, HumanOnLoop, FullyAutonomous]
  # HumanInLoop: human approves every action
  # HumanOnLoop: human can intervene; agent acts autonomously by default
  # FullyAutonomous: no human checkpoint in normal operation

  # ── Composition ───────────────────────────────────────────────
  primary_model: ModelRef           # model that handles the primary reasoning
  fallback_models: ModelRef[]       # models used when primary is unavailable
  tool_set: ToolRef[]               # all tools this agent is authorized to call
  sub_agents: AgentRef[]            # orchestrated sub-agents (for multi-agent)
  knowledge_sources: KnowledgeSourceRef[]
  prompt_set: PromptRef[]           # all prompts used by this agent

  # ── Data Governance ───────────────────────────────────────────
  data_classification: enum[Public, Internal, Confidential, Restricted, TopSecret]
  pii_handling:
    processes_pii: boolean
    pii_categories: string[]        # e.g., [EmployeeName, ContactInfo]
    pii_handling_policy: PolicyRef
  data_retention_policy: RetentionPolicyRef
  data_residency_requirements: string[]  # e.g., [EU, US]
  mnpi_exposure: boolean            # does agent handle material non-public information?

  # ── Risk ──────────────────────────────────────────────────────
  risk_profile: RiskProfileRef
  max_execution_depth: int          # max tool call chain depth before circuit break
  human_escalation_policy:
    escalation_triggers: string[]
    escalation_contact: PersonRef
  circuit_breaker:
    enabled: boolean
    error_threshold: float
    time_window_seconds: int
    cooldown_seconds: int

  # ── Compliance ────────────────────────────────────────────────
  applicable_frameworks: ComplianceFrameworkRef[]
  certifications: CertificationRef[]
  regulatory_scope: string          # e.g., "Investment Advisory", "Research"
  explainability_requirement: enum[None, Basic, Full, Regulatory]

  # ── Lifecycle ─────────────────────────────────────────────────
  status: enum[Development, Staging, CertificationReview, Certified,
               Production, Deprecated, Retired]
  deployment_record: DeploymentRecord[]
  deprecation_plan: DeprecationPlan   # required before retiring

  # ── Audit ─────────────────────────────────────────────────────
  created_at: datetime
  created_by: PersonRef
  last_modified: datetime
  last_modified_by: PersonRef
  modification_history: ChangeEvent[]
```

---

## Required Fields for Registration

Minimum fields that MUST be present before an agent can be registered:

| Field | Reason |
|-------|--------|
| canonical_name | Stable identity across versions |
| business_owner | Accountability |
| technical_owner | Technical accountability |
| agent_type | Determines applicable policies |
| autonomy_level | Determines risk tier minimum |
| primary_model | Model governance dependency |
| data_classification | Data handling policy selection |
| use_case | Compliance scope determination |

---

## Ownership Transfer Process

Ownership is not self-assignable. Transfer requires:
1. Current owner submits transfer request with successor
2. Successor acknowledges acceptance of governance obligations
3. Governance review approves the transfer
4. Audit event recorded with both parties' acknowledgment

Agents without active owners enter a governance hold: they cannot be modified or redeployed
until ownership is resolved.
