# Prompt Metadata Model

## Why Prompts Are Enterprise Assets

Prompts are not configuration parameters. In an enterprise context, a prompt is:

- The primary instruction governing AI behavior — more influential than model choice
- The primary attack surface for prompt injection and jailbreak attacks
- The principal determinant of output quality, consistency, and safety
- A carrier of proprietary business logic and methodology (IP risk)
- A material factor in regulatory explainability requirements
- A versioned artifact that, when changed, may invalidate safety certifications

When a prompt is changed, the AI system's behavior changes. That change may violate
compliance requirements, introduce new biases, invalidate previous evaluations, or
expose confidential business logic. Prompts must be governed with the same discipline
as production software code.

---

## Complete Schema

```yaml
PromptRecord:
  # ── Identity ──────────────────────────────────────────────────
  prompt_id: UUID
  canonical_name: string            # org.team.prompt-name
  version: semver
  display_name: string
  description: string               # what this prompt does and why

  # ── Classification ────────────────────────────────────────────
  prompt_type: enum[System, User, FewShot, ChainOfThought, Tool,
                    RetrievalAugmented, SafetyCheck, Evaluator]
  domain: string                    # e.g., "valuation", "credit-analysis"
  purpose: string                   # detailed business purpose

  # ── Content Governance ────────────────────────────────────────
  # NOTE: Prompt content (template) is stored encrypted and accessed
  # only by authorized runtime systems. The metadata record does NOT
  # contain the actual prompt text in cleartext.
  content_hash: sha256              # hash of encrypted content, for integrity
  content_version_id: string        # reference to encrypted content store
  variables: VariableSpec[]         # declared input variables with types
  examples: ExampleSet[]            # few-shot examples (separately versioned)
  approximate_token_count: int      # estimated token consumption

  # ── Quality ───────────────────────────────────────────────────
  evaluation_results: EvaluationRef[]
  latest_scorecard: ScorecardRef
  hallucination_risk_score: float   # 0.0 – 10.0 from evaluation
  prompt_injection_assessment:
    risk_level: enum[Low, Medium, High, Critical]
    assessed_by: PersonRef
    assessed_at: datetime
    vulnerabilities_found: string[]
    mitigations_applied: string[]

  # ── Ownership ─────────────────────────────────────────────────
  owning_team: TeamRef
  author: PersonRef
  subject_matter_expert: PersonRef  # domain expert who validates correctness

  # ── Dependencies ──────────────────────────────────────────────
  consuming_agents: AgentRef[]      # agents using this prompt
  consuming_workflows: WorkflowRef[]

  # ── Data Sensitivity ──────────────────────────────────────────
  data_sensitivity: enum[None, Low, Medium, High]
  contains_pii_handling_instructions: boolean
  contains_proprietary_methodology: boolean
  contains_regulatory_language: boolean

  # ── Lifecycle ─────────────────────────────────────────────────
  status: enum[Draft, PeerReview, Evaluation, InjectionReview,
               ApprovalPending, Approved, Active, Deprecated, Retired]
  approval_record: ApprovalRef
  rollback_target: PromptRef        # nullable — version to roll back to if needed
  deprecation_plan: DeprecationPlan

  # ── Audit ─────────────────────────────────────────────────────
  created_at: datetime
  created_by: PersonRef
  last_modified: datetime
  last_modified_by: PersonRef
  modification_history: ChangeEvent[]
```

---

## Prompt Versioning and Approval Matrix

| Version Change | Approval Required | Evaluation Required | Injection Review |
|---------------|-----------------|-------------------|-----------------|
| Patch (1.0.X) | Team lead | Abbreviated re-run | Only if instruction changed |
| Minor (1.X.0) | Governance reviewer | Full benchmark run | Yes |
| Major (X.0.0) | Committee review | Full + human evaluation | Full security review |

---

## Prompt Rollback

Prompt rollback is a first-class operation available to authorized users:

```
Immediate rollback: revert to previous Active version — one API call
Targeted rollback: revert to any historical version — specify version
Canary rollback: route a percentage of traffic to previous version
Auto-rollback trigger: if evaluation score drops below threshold post-deployment
```

All rollbacks generate audit events with the triggering reason and authorizing actor.

---

## Prompt Lifecycle

```
DRAFT (local development)
  │
  ▼ submit for review
PEER_REVIEW (team review, code review of prompt logic)
  │
  ▼ submit for evaluation
EVALUATION (automated benchmark evaluation)
  │
  ▼ submit for security
INJECTION_REVIEW (prompt injection vulnerability assessment)
  │
  ▼ submit for approval
APPROVAL_PENDING (governance approval workflow)
  │
  ▼ approved
ACTIVE (deployed in production, continuously monitored)
  │
  ├──► CHANGE_REQUEST ──────────────────────► back to DRAFT (new version)
  ├──► INCIDENT ──► EMERGENCY_REVIEW ──► ROLLBACK or PATCH
  └──► DEPRECATION ──► DEPRECATED ──► RETIRED
```
