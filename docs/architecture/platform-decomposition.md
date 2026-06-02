# Platform Decomposition

## Service Decomposition

Each bounded service has a single responsibility, a stable API contract, and independent
deployability. Services communicate asynchronously via the Governance Event Bus for
non-blocking operations and synchronously via REST for critical-path operations.

| Service | Domain | Criticality | Owns |
|---------|--------|-------------|------|
| governance-gateway | API | Critical Path | Routing, auth, rate limiting |
| policy-service | Policy Plane | Critical Path | Policy store, compiler, evaluator |
| registry-service | Registry System | Critical Path | Artifact metadata, status |
| audit-service | Evidence System | Critical Path | Immutable event log |
| risk-service | Risk Plane | Near-Critical | Risk scoring, thresholds |
| compliance-service | Compliance Plane | Near-Critical | Control mapping, posture |
| evaluation-service | Evaluation Plane | Asynchronous | Benchmark execution, scorecards |
| approval-service | Approval Plane | Asynchronous | Workflow routing, decisions |
| security-service | Security Plane | Critical Path (inline) | Threat detection, classification |
| observability-service | Observability Plane | Near-Critical | Telemetry, anomaly detection |
| lineage-service | Evidence System | Asynchronous | Lineage graph, provenance |
| notification-service | Cross-cutting | Asynchronous | Event subscriptions, alerts |
| tenant-management-service | Multi-tenancy | Administrative | Tenant provisioning |

---

## Service Dependency Graph

```
governance-gateway
    ├── policy-service         (synchronous, inline evaluation)
    ├── registry-service       (synchronous, artifact lookup)
    ├── audit-service          (asynchronous, fire-and-forget)
    └── security-service       (synchronous, inline check)

policy-service
    ├── registry-service       (artifact metadata for evaluation context)
    └── audit-service          (policy change events)

registry-service
    ├── risk-service           (triggers risk assessment on registration)
    ├── evaluation-service     (triggers evaluation on registration)
    ├── approval-service       (routes to approval on registration)
    └── audit-service          (registration events)

risk-service
    ├── compliance-service     (compliance posture informs risk)
    ├── evaluation-service     (evaluation results inform risk)
    └── audit-service          (risk change events)

approval-service
    ├── policy-service         (policy compliance check before approval)
    ├── risk-service           (risk score determines approval tier)
    ├── evaluation-service     (evaluation clearance required for approval)
    └── audit-service          (approval decisions)

observability-service
    ├── risk-service           (behavioral anomalies → risk re-assessment)
    ├── evaluation-service     (production signals → evaluation triggers)
    └── notification-service   (threshold breach alerts)
```

---

## Governance Maturity Model

### Level 1 — Reactive
- No central registry; artifacts tracked in spreadsheets or not at all
- Governance is post-incident investigation
- No platform-level audit capability
- Policies exist as documents; enforcement is manual

### Level 2 — Defined
- Registry exists but registration is partially voluntary
- Written policies exist; enforcement is manual review
- Basic audit logging in application logs (not centralized)
- Evaluation present for some artifacts, not systematic

### Level 3 — Managed (Platform-Driven)
- Mandatory registration enforced via platform dependency
- Policy engine handles Tier 1 deployments automatically
- Centralized, queryable audit trail with full governance coverage
- Systematic evaluation with regression detection
- Quantitative risk scoring; risk tiers drive approval workflows
- 70%+ of deployments receive automated clearance

### Level 4 — Optimizing (Intelligence-Driven)
- Predictive risk: platform anticipates risk changes before they materialize
- Proactive compliance: regulatory changes automatically assessed against inventory
- Self-healing: common issues trigger automated remediation without human intervention
- Cross-tenant intelligence: aggregate patterns inform platform improvements
- Developer experience excellence: clearance in minutes, high satisfaction scores

### Level 5 — Leading (Ecosystem-Defining)
- Industry standard contributions: benchmarks and methodologies adopted by peers
- Regulatory recognition: platform certifications treated as credible examination evidence
- Federated governance: capability extends beyond firm boundaries
- AI-assisted governance: specialized AI models assist policy and risk teams
- Governance as revenue: capabilities offered as distinct enterprise value proposition

---

## Anti-Patterns to Avoid

| Anti-Pattern | Description | Prevention |
|---|---|---|
| Governance Checkbox | Governance exists to satisfy auditors, not govern | Measure quality of decisions, not presence |
| Policy Explosion | Uncontrolled policy proliferation | Policy owners, sunset process, regular audits |
| Governance Silos | Security, MRM, data, AI governance in separate tools | Unified platform with integrations |
| Shadow AI | Teams bypass governance via personal API keys | Make governed path cheaper than shadow path |
| Governance Debt Spiral | "We'll add governance later" → never comes | Governance in CI/CD from day one |
| Waterfall Governance | Heavyweight manual review for every change | Continuous automated clearance |
