# Self-Service Governance Model

## The Core Principle

Centralized review does not scale. At 100+ teams and thousands of agents, human review
of every deployment is impossible without becoming a bottleneck that incentivizes shadow AI.

The self-service governance model inverts the burden:
- **Platform publishes** policies, risk models, and compliance controls
- **Teams apply** those standards to their own artifacts using self-service tooling
- **Platform validates** compliance automatically
- **Human review** is reserved for exceptions, high-risk artifacts, and novel patterns

This model handles 70-80% of deployments through fully automated clearance.

---

## The Three-Tier Self-Service Model

### Tier 1: Automated Clearance (~70-80% of deployments)

Criteria for automatic clearance:
- All policy requirements met by declared manifest
- Risk score ≤ 4.0 (Low or Minimal tier)
- Uses pre-certified models
- Consumes approved datasets
- Evaluation benchmarks pass
- No novel tool integrations

Experience for the team:
```
$ governance-cli submit --manifest agent-manifest.yaml

✓  Artifact registered: agent-id = 9f3c-a8b2-...
✓  Policy evaluation: ALL PASSED (14/14 checks)
✓  Risk assessment: Composite score 2.8 (LOW RISK)
✓  Evaluation: PASSED (accuracy: 0.91, hallucination: 0.018, safety: 0.97)
✓  Governance clearance: APPROVED (automated)

Artifact is cleared for deployment. Artifact ID: 9f3c-a8b2-...
```

Total time: ~3 minutes.

### Tier 2: Assisted Review (~15-20% of deployments)

Triggered when:
- Minor policy gaps that require documentation
- Risk score 4.1–6.0 (Moderate tier)
- Novel prompt patterns not previously evaluated
- Newly onboarded model version

Experience for the team:
```
$ governance-cli submit --manifest agent-manifest.yaml

✓  Artifact registered
⚠  Policy evaluation: 12/14 passed, 2 require documentation
⚠  Risk assessment: Composite score 5.1 (MODERATE RISK)
✓  Evaluation: PASSED

Governance clearance: UNDER REVIEW
Assigned to: governance-reviewer@firm.com
Estimated SLA: 2 business days
Review package: governance.firm.com/review/REQ-4821

Action required from you:
  1. Address policy gap: data_retention_policy not specified (see Policy PRI-012)
  2. Document rationale for using GPT-4o-preview (not yet certified for this use case)
```

### Tier 3: Committee Review (~5% of deployments)

Triggered when:
- Risk score > 6.0 (High or Critical)
- Novel model integration (not previously onboarded)
- Workflow touches MNPI data
- Investment decision-making with regulatory exposure
- Exception to a platform policy requested

Experience: Structured review process with Risk, Compliance, and Security sign-off.
Team receives detailed review package and specific questions to address.

---

## Developer Portal Capabilities

The Developer Portal is the primary interface for self-service governance:

| Feature | What it does |
|---------|-------------|
| Policy Explorer | Discover which policies apply to your artifact before building |
| Risk Estimator | Get a preliminary risk score based on your intended architecture |
| Manifest Builder | Guided form for creating a governance manifest |
| Governance Status | Real-time view of your artifact's governance posture |
| Approval Tracker | Track pending reviews and respond to reviewer questions |
| Evaluation History | View all evaluation results for your artifacts |
| Compliance Dashboard | Your team's compliance posture against applicable frameworks |
| Cost Dashboard | Your team's AI spend and budget consumption |

---

## How Product Teams Interact with Governance

```
BEFORE BUILDING:
  → Browse Policy Explorer to understand what policies apply
  → Use Risk Estimator to check if architecture will pass automated clearance
  → Review example manifests from similar approved artifacts

DURING DEVELOPMENT:
  → Write governance manifest alongside the artifact
  → Run governance-cli validate --manifest ... for local validation
  → Check evaluation benchmarks are available for your use case domain

AT DEPLOYMENT:
  → governance-cli submit → receive clearance or review requirements
  → Address any gaps, re-submit for re-evaluation
  → On clearance: deploy using platform credentials

IN PRODUCTION:
  → Subscribe to governance events for your artifact (policy changes, risk alerts)
  → Monitor compliance posture via team dashboard
  → Respond to re-certification requests before expiry
  → Report governance issues via governance-cli incident ...
```

---

## Developer Experience Metrics

The Governance Platform tracks DX as rigorously as compliance:

| Metric | Target | Measured Weekly |
|--------|--------|----------------|
| Median time to Tier 1 clearance | < 5 minutes | Yes |
| P90 time to Tier 2 clearance | < 2 business days | Yes |
| Self-service success rate | > 75% (Tier 1 without rework) | Yes |
| Developer satisfaction score | > 4.0 / 5.0 | Monthly survey |
| Support ticket volume | Trending down quarter-over-quarter | Yes |
