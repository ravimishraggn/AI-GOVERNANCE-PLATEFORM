# Approval Plane

## Purpose

The Approval Plane orchestrates the human review workflows required for governance decisions
that cannot be automated: high-risk artifact certifications, novel model integrations,
compliance exception requests, and escalated policy overrides.

---

## Responsibilities

- Route governance review requests to appropriate human reviewers based on artifact risk tier
- Track approval state through multi-stage workflows with configurable steps, SLAs, escalations
- Collect structured review decisions with mandatory justification
- Enforce dual-control requirements for high-risk decisions
- Maintain a complete record of all approval decisions and their rationale
- Integrate with enterprise identity to validate approver authorization
- Generate approval summary metrics for governance reporting

---

## Approval Tiers

| Tier | Risk Score | Approver | Typical SLA | Notes |
|------|-----------|---------|------------|-------|
| Tier 1 | 0.0–4.0 | Automated | Minutes | 70–80% of deployments |
| Tier 2 | 4.1–6.0 | Team lead + Governance reviewer | 1–3 days | Assisted review |
| Tier 3 | 6.1–10.0 | Committee: Risk + Compliance + Security | 5–10 days | Full review |

---

## Data Model

```yaml
ApprovalRequest:
  id: UUID
  artifact: ArtifactRef
  artifact_version: semver
  request_type: enum[Registration, Deployment, PolicyException, ModelCertification,
                     PromptPromotion, WorkflowCertification, RiskAcceptance]
  requester: UserRef
  submitted_at: datetime
  required_approvers: ApproverSpec[]
  current_stage: WorkflowStage
  sla_deadline: datetime
  review_package: ReviewPackageRef   # automated analysis prepared by platform
  decisions: ApprovalDecision[]
  final_outcome: enum[Approved, Rejected, Escalated, Withdrawn, Expired, ConditionallyApproved]
  conditions: ApprovalCondition[]    # conditions placed on approval
  audit_record: AuditEventRef

ApprovalDecision:
  approver: UserRef
  role: ApproverRole
  decision: enum[Approve, Reject, RequestChanges, Abstain, Escalate]
  rationale: string                  # required — cannot approve without rationale
  conditions: string
  timestamp: datetime
  signature: digital_signature       # cryptographic signature by approver

WorkflowTemplate:
  name: string
  applicable_to: ArtifactCriteria   # which artifacts use this template
  stages: WorkflowStage[]
  escalation_rules: EscalationRule[]
  sla_policy: SLAPolicy
  dual_control_required: boolean    # for highest-risk decisions
  minimum_approvers: int
```

---

## Review Package Contents

The platform automatically prepares a structured review package for every approval request:

- Artifact governance manifest summary
- Risk assessment report with factor breakdown
- Policy compliance report (which policies pass, which fail, which require exception)
- Evaluation scorecard summary
- Compliance posture against applicable frameworks
- Similar previously approved artifacts (precedent analysis)
- Recommended approval tier and rationale
- Specific questions the reviewer should address

The review package reduces review time by presenting the governance analysis upfront.
Reviewers focus on judgment, not information gathering.

---

## Services Exposed

| Method | Signature | SLA |
|--------|-----------|-----|
| SubmitApprovalRequest | `(artifact, request_type) → ApprovalRequest` | P99 < 500ms |
| GetPendingReviews | `(approver, filters) → ApprovalRequest[]` | P99 < 200ms |
| SubmitDecision | `(request_id, decision) → ApprovalDecision` | P99 < 500ms |
| GetApprovalStatus | `(artifact) → ApprovalStatus` | P99 < 200ms |
| ConfigureWorkflowTemplate | `(criteria, template) → WorkflowTemplate` | Async |
| EscalateRequest | `(request_id, reason) → EscalationRecord` | P99 < 200ms |
| GetApprovalMetrics | `(scope, period) → ApprovalMetrics` | Async |

---

## SLA Enforcement

- SLA deadlines tracked with automated reminders at 50% and 80% of SLA elapsed
- At 100%: automatic escalation to next approver level
- At 150%: notification to Governance Platform team for SLA breach reporting
- Governance reporting includes SLA compliance rate as a key metric

---

## Extension Points

- Custom workflow templates for new artifact types
- Integration with enterprise task management (Jira, ServiceNow)
- Custom approver role definitions with dynamic authorization logic
- External notification integrations (Slack, Teams, email) for approval requests
