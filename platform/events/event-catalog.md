# Governance Event Catalog

All governance events emitted by the platform. Product teams subscribe to events
relevant to their artifacts via the Notification Service.

---

## Event Format

All events follow a standard envelope:

```json
{
  "event_id": "uuid",
  "event_type": "policy.changed",
  "timestamp": "2026-05-31T10:00:00Z",
  "version": "1.0",
  "source": "governance-platform",
  "tenant_id": "tenant-uuid",
  "subject": {
    "type": "agent",
    "id": "artifact-uuid"
  },
  "data": { /* event-specific payload */ }
}
```

---

## Policy Events

| Event Type | Trigger | Typical Consumer |
|-----------|---------|----------------|
| `policy.published` | New policy version published | Governance team |
| `policy.activated` | Policy becomes effective | All affected artifacts |
| `policy.changed` | Active policy content changed | CI/CD pipelines, artifact owners |
| `policy.deprecated` | Policy marked for retirement | Governance team |
| `policy.evaluated` | Policy evaluated for an artifact | Audit service |
| `policy.violation` | Policy evaluation returned BLOCK | Security team, artifact owner |
| `policy.exception.granted` | Exception approved | Artifact owner |
| `policy.exception.expiring` | Exception expires within 14 days | Artifact owner |
| `policy.exception.expired` | Exception has expired | Artifact owner, governance team |

## Risk Events

| Event Type | Trigger | Typical Consumer |
|-----------|---------|----------------|
| `risk.profile.computed` | Risk score computed for artifact | Registry service |
| `risk.score.changed` | Risk score changed significantly | Artifact owner, risk team |
| `risk.threshold.breached` | Score crossed a tier threshold | Artifact owner, risk team |
| `risk.acceptance.granted` | Risk acceptance recorded | Artifact owner |
| `risk.acceptance.expiring` | Acceptance expires within 30 days | Artifact owner |
| `risk.acceptance.expired` | Acceptance has expired | Artifact owner, risk team |
| `risk.reassessment.triggered` | Reassessment job queued | Risk team |
| `risk.reassessment.completed` | Reassessment job finished | Artifact owner |

## Artifact Lifecycle Events

| Event Type | Trigger | Typical Consumer |
|-----------|---------|----------------|
| `artifact.registered` | New artifact registered | Governance team |
| `artifact.updated` | Artifact metadata updated | Dependent services |
| `artifact.version.published` | New version registered | Evaluation service |
| `artifact.status.changed` | Lifecycle status changed | Artifact owner |
| `artifact.deployed` | Artifact promoted to production | Observability service |
| `artifact.deprecated` | Artifact marked deprecated | Consuming artifacts |
| `artifact.retired` | Artifact fully retired | All consumers |
| `artifact.ownership.changed` | Owner changed | New owner, governance team |

## Model Events

| Event Type | Trigger | Typical Consumer |
|-----------|---------|----------------|
| `model.version.available` | New model version from provider | Platform engineering |
| `model.certification.completed` | MRM certification decision | Artifact owners using model |
| `model.deprecation.announced` | Provider announces deprecation | All agents using model |
| `model.retired` | Model no longer usable on platform | All agents using model |

## Approval Events

| Event Type | Trigger | Typical Consumer |
|-----------|---------|----------------|
| `approval.request.submitted` | New approval request | Assigned reviewers |
| `approval.decision.made` | Reviewer submits decision | Requestor |
| `approval.escalated` | Request escalated | New assignee |
| `approval.sla.warning` | SLA at 80% elapsed | Current reviewers |
| `approval.sla.breached` | SLA elapsed | Governance team, management |
| `approval.expired` | Request expired without decision | Requestor |

## Certification Events

| Event Type | Trigger | Typical Consumer |
|-----------|---------|----------------|
| `certification.issued` | Artifact certified | Artifact owner |
| `certification.expiring` | Expires within 30 days | Artifact owner, governance team |
| `certification.expired` | Certification has expired | Artifact owner (deployment blocked) |
| `certification.revoked` | Certification revoked (e.g., incident) | Artifact owner |

## Security Events

| Event Type | Trigger | Typical Consumer |
|-----------|---------|----------------|
| `security.injection.detected` | Prompt injection attempt | Security team, artifact owner |
| `security.jailbreak.attempted` | Jailbreak attempt detected | Security team |
| `security.exfiltration.suspected` | Data exfiltration pattern | Security team (immediate) |
| `security.anomaly.detected` | Behavioral anomaly | Security team, artifact owner |
| `security.incident.raised` | Formal incident created | Security team, SIEM |

## Evaluation Events

| Event Type | Trigger | Typical Consumer |
|-----------|---------|----------------|
| `evaluation.job.completed` | Evaluation run finished | Artifact owner |
| `evaluation.regression.detected` | Regression found vs. baseline | Artifact owner, risk team |
| `evaluation.regression.critical` | Safety regression detected | Artifact owner, security, risk |
| `evaluation.benchmark.updated` | Benchmark version changed | All artifacts using benchmark |

## Compliance Events

| Event Type | Trigger | Typical Consumer |
|-----------|---------|----------------|
| `compliance.gap.detected` | Control gap identified | Compliance officer, artifact owner |
| `compliance.gap.remediated` | Gap closed | Compliance officer |
| `compliance.posture.degraded` | Overall posture dropped | Compliance officer |
| `compliance.exception.granted` | Exception approved | Artifact owner |
| `compliance.regulatory.change` | New regulation or guidance | Compliance team, all tenants |
| `compliance.evidence.generated` | Evidence package ready | Compliance officer |

## Observability Events

| Event Type | Trigger | Typical Consumer |
|-----------|---------|----------------|
| `cost.budget.warning` | Budget at 80% consumed | Team lead, finance |
| `cost.budget.exceeded` | Budget exceeded | Team lead, finance (blocks new deployments) |
| `cost.anomaly.detected` | Unusual cost spike | Team lead, platform ops |
| `quality.drift.detected` | Quality metrics drifting | Artifact owner, evaluation team |
| `latency.sla.breached` | Latency SLA exceeded | Platform SRE, artifact owner |
