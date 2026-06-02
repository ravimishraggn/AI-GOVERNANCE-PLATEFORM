# Tool Metadata Model

## Why Tools Require Governance

When an AI agent calls a tool, it crosses from the language model domain into the real
world. Tools write data, call external APIs, execute computations, and trigger business
processes. The governance implications are severe:

- A tool call may produce irreversible side effects
- A tool may access sensitive data beyond what the agent is authorized to see
- A tool may be used by a compromised agent to exfiltrate data or cause harm
- Tool calls generate audit-relevant events that must be recorded and attributable

Every tool must be registered, reviewed, and authorized before any agent can invoke it.

---

## Complete Schema

```yaml
ToolRecord:
  # Identity
  tool_id: UUID
  canonical_name: string
  version: semver
  display_name: string
  description: string

  # Classification
  tool_type: enum[DataRetrieval, Computation, ExternalAPI, FileSystem,
                  DatabaseQuery, Communication, Orchestration, CodeExecution]
  idempotent: boolean                # can the tool be called multiple times safely?
  reversible: boolean                # can the tool's effects be undone?
  side_effects: string[]             # list of real-world effects this tool produces

  # Interface
  input_schema: json_schema
  output_schema: json_schema
  error_schema: json_schema

  # Security
  required_permissions: string[]     # platform permissions required to call this tool
  data_access_scope: string[]        # what data stores this tool can access
  network_access_required: boolean
  external_systems: ExternalSystemRef[]  # which external systems this tool calls
  credential_requirements: string[]

  # Risk
  risk_tier: enum[Minimal, Low, Moderate, High, Critical]
  security_review: SecurityReviewRef
  security_review_date: date
  threat_surface: string[]           # attack vectors relevant to this tool

  # Authorization
  approved_callers: AgentRef[]       # agents explicitly approved to call this tool
  # Note: an agent not in this list cannot call this tool even if it tries
  prohibited_use_cases: string[]

  # Operational
  rate_limits:
    calls_per_minute: int
    calls_per_agent_per_minute: int
  timeout_policy:
    soft_timeout_ms: int             # warn after this
    hard_timeout_ms: int             # kill after this
  retry_policy:
    max_retries: int
    backoff_strategy: string

  # Lifecycle
  status: enum[Development, Review, Approved, Active, Deprecated, Retired]
  owner: TeamRef
  created_at: datetime
  last_security_review: datetime
```

---

## Tool Risk Tier Definitions

| Tier | Examples | Approval Required |
|------|---------|------------------|
| Minimal | Read-only data lookup, public API | Automated |
| Low | Internal DB query (read-only), file read | Team lead |
| Moderate | Write to internal system, external API call | Governance review |
| High | Database write, email/notification send | Committee review |
| Critical | Financial transaction, regulatory filing | Executive approval |
