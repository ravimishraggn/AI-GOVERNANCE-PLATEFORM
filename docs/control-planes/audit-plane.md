# Audit Plane

## Purpose

The Audit Plane maintains an immutable, cryptographically tamper-evident record of every
significant event in the AI platform's lifecycle. It is the court of record for the
enterprise's AI governance — the system that makes six-month-old AI decisions explainable.

---

## Design Principles

**Completeness Over Selectivity**
Record all governance-relevant events. The instinct to skip "routine" events is a
governance failure waiting to happen. Storage cost is trivially small relative to
missing audit evidence at an examination.

**Immutability Is Non-Negotiable**
Audit records that can be modified after the fact are worthless as evidence. Each event
is cryptographically chained — every event includes the hash of the prior event. Any
modification to any past record breaks the chain, making tampering detectable.

**Separation of Concerns**
Audit records are stored and managed independently from the systems they audit.
The audit store is administered by the Governance Team, not application teams.

**Queryability at Scale**
An audit record that cannot be queried efficiently is operationally useless.
The store must support forensic queries across billions of events by artifact, actor,
period, and event type in seconds, not minutes.

---

## Data Model

```yaml
AuditEvent:
  id: UUID
  sequence_number: int64        # monotonically increasing per tenant
  event_type: AuditEventType
  event_timestamp: datetime     # UTC, nanosecond precision
  actor:
    actor_type: enum[User, System, Agent, ExternalService]
    actor_id: string
    actor_tenant: TenantRef
  subject:
    subject_type: ArtifactType
    subject_id: ArtifactRef
    subject_version: semver
  action: string
  outcome: enum[Success, Failure, Partial]
  policy_context:               # snapshot of policy state at event time
    applicable_policies: PolicyVersionRef[]
    evaluation_result: PolicyDecision
    exceptions_active: ExceptionRef[]
  risk_context:                 # snapshot of risk state at event time
    composite_score: float
    risk_tier: RiskTier
    acceptance_active: RiskAcceptanceRef
  compliance_context:           # snapshot of compliance state at event time
    frameworks: FrameworkRef[]
    posture: enum[Compliant, NonCompliant, AtRisk]
  event_data: encrypted_json    # event-specific payload, encrypted at rest
  previous_hash: sha256
  event_hash: sha256            # hash of this event's content
  signature: digital_signature  # signed by Governance Platform HSM key
  retention_class: RetentionPolicy
  tenant_id: TenantRef
```

---

## Audit Event Types

```
Artifact lifecycle:  ArtifactRegistered, ArtifactUpdated, ArtifactDeployed,
                     ArtifactDeprecated, ArtifactRetired

Policy:             PolicyPublished, PolicyActivated, PolicyEvaluated,
                     PolicyViolation, PolicyException, PolicyRetired

Risk:               RiskAssessmentCompleted, RiskScoreChanged,
                     RiskThresholdBreached, RiskAcceptanceGranted,
                     RiskAcceptanceExpired

Approval:           ApprovalRequested, ApprovalDecisionMade,
                     ApprovalEscalated, ApprovalWithdrawn

Security:           PromptInjectionDetected, JailbreakAttempted,
                     DataExfiltrationAttempted, SecurityIncidentRaised

Execution:          AgentInvoked, ModelCalled, ToolCalled,
                     WorkflowStarted, WorkflowCompleted,
                     HumanEscalationTriggered

Compliance:         ComplianceGapDetected, ComplianceGapRemediated,
                     ComplianceExceptionGranted, EvidencePackageGenerated

Configuration:      TenantConfigChanged, PolicySetChanged,
                     RiskModelChanged, ApprovalWorkflowChanged
```

---

## Services Exposed

| Method | Signature | SLA |
|--------|-----------|-----|
| RecordAuditEvent | `(event) → AuditEventRecord` | Fire-and-forget, async, < 5ms |
| QueryAuditTrail | `(artifact, period, event_types) → AuditTrail` | P99 < 2s |
| ReconstructState | `(artifact, as_of_timestamp) → ArtifactStateSnapshot` | P99 < 5s |
| VerifyIntegrity | `(audit_trail) → IntegrityReport` | Async |
| GenerateAuditReport | `(scope, period, format) → AuditReport` | Async |
| ExportAuditEvidence | `(query, recipient) → EvidenceExport` | Async, authorized |

---

## Answering the Six-Month Question

To explain any AI decision made six months ago:

1. Query AuditTrail for the execution event (AgentInvoked, ModelCalled, etc.)
2. Retrieve execution record: artifact version, model version, prompt version, user
3. Retrieve `policy_context` snapshot: which policies were active, what was the decision
4. Retrieve `risk_context` snapshot: what risk score was accepted
5. For RAG: retrieve content lineage (which documents were in context)
6. For agentic: retrieve tool call history from execution event chain
7. Package as human-readable evidence report via GenerateAuditReport

Time to reconstruct: minutes via portal, not weeks via engineering investigation.

---

## Retention Policies

| Event Class | Minimum Retention | Driver |
|-------------|------------------|--------|
| Execution events | 7 years | SEC Rule 17a-4, FINRA 4511 |
| Policy evaluations | 7 years | SR 11-7 model documentation |
| Approval decisions | 7 years + 3 years post-retirement | Legal hold |
| Security events | 3 years | SOC 2, internal control |
| Configuration changes | Indefinite | Regulatory examination |
| Compliance evidence | Per framework requirement | Framework-specific |

---

## Integrity Architecture

- Every event is signed by the Governance Platform's signing key (HSM-backed)
- Events are cryptographically chained: each event contains the hash of the prior event
- Chains are periodically anchored (e.g., Merkle tree root published to immutable log)
- Any tampering with any historical event breaks the chain and is detectable
- The verification API (`VerifyIntegrity`) can validate any audit trail on demand
