# Workflow Metadata Model

## Schema

```yaml
WorkflowRecord:
  # Identity
  workflow_id: UUID
  canonical_name: string
  version: semver
  display_name: string
  description: string
  business_process: string          # the business process this workflow implements

  # Structure
  workflow_type: enum[Sequential, Parallel, Conditional, Loop,
                      HumanInLoop, MultiAgent, EventDriven]
  steps: WorkflowStep[]
  entry_triggers: TriggerSpec[]
  exit_conditions: ExitCondition[]

  # Composition
  agents_used: AgentRef[]
  models_used: ModelRef[]
  tools_used: ToolRef[]
  datasets_accessed: DatasetRef[]
  knowledge_sources: KnowledgeAssetRef[]

  # Risk
  workflow_risk_profile: RiskProfileRef
  human_escalation_policy:
    required_at_steps: string[]
    escalation_contacts: PersonRef[]
  max_execution_depth: int          # prevents infinite loops
  max_execution_duration_minutes: int
  circuit_breaker:
    enabled: boolean
    failure_threshold: float
    observation_window_seconds: int

  # Compliance
  approval_gates: ApprovalGate[]    # steps requiring explicit human approval
  compliance_checkpoints: ComplianceCheckpoint[]
  audit_checkpoints: AuditCheckpoint[]
  data_handling_policy: DataHandlingPolicyRef

  # Operational
  sla:
    expected_duration_minutes: int
    p99_duration_minutes: int
    breach_action: string
  cost_budget:
    max_cost_usd_per_execution: float
    budget_exceeded_action: enum[Warn, Block, Escalate]
  timeout: duration

  # Ownership and Lifecycle
  owner: TeamRef
  status: enum[Development, Staging, Certified, Production, Deprecated, Retired]
  approval_record: ApprovalRef
  created_at: datetime
  last_modified: datetime

WorkflowStep:
  step_id: string
  step_type: enum[AgentCall, ModelCall, ToolCall, HumanTask, Conditional, Loop]
  artifact_ref: ArtifactRef         # which agent/model/tool
  inputs: InputMapping
  outputs: OutputMapping
  governance_checkpoints: GovernanceCheckpoint[]
  audit_required: boolean
```

---

## Workflow Governance Checkpoints

At each governance checkpoint, the workflow engine:
1. Records a workflow-step audit event
2. Evaluates applicable policies against the current state
3. Checks cost consumption against budget
4. Evaluates safety signals from the step's output
5. Checks whether human escalation is required
