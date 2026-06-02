# Risk Plane

## Purpose

The Risk Plane maintains the enterprise AI risk model, scores every registered artifact
against that model, tracks risk posture over time, and enforces risk-based deployment gates.

---

## Responsibilities

- Maintain the canonical AI risk taxonomy: agent, model, data, prompt, workflow, regulatory
- Score every registered artifact on a multi-dimensional risk profile
- Aggregate artifact-level risks into workflow, team, tenant, and platform posture
- Monitor for risk changes triggered by behavioral data, external events, or config changes
- Enforce risk thresholds as hard deployment gates and soft monitoring alerts
- Maintain risk acceptance records: who accepted what risk, when, and for how long
- Feed risk signals to Compliance, Approval, and Observability planes

---

## Risk Taxonomy (Top Level)

```
Agent Risk
  ├── Autonomy Risk         probability agent takes unintended consequential actions
  ├── Escalation Risk       probability agent creates action chains beyond design
  ├── Tool Misuse Risk      probability agent invokes tools causing unintended effects
  ├── Loop Risk             probability agent enters pathological execution patterns
  └── Trust Propagation     probability compromised agent spreads to multi-agent network

Model Risk
  ├── Hallucination Risk    tendency to generate plausible but false outputs
  ├── Bias Risk             systematic patterns disadvantaging specific groups
  ├── Capability Boundary   gap between apparent and actual reliable capabilities
  ├── Alignment Risk        divergence between model optimization and intended use
  └── Provider Dependency   operational risk from single LLM provider reliance

Data Risk
  ├── Sensitivity Risk      confidentiality classification of accessed data
  ├── Leakage Risk          probability sensitive data exposed through outputs
  ├── Poisoning Risk        adversarial content corrupting model behavior
  ├── Staleness Risk        outdated data causing materially incorrect outputs
  └── Lineage Risk          inability to trace data origins (regulatory exposure)

Prompt Risk
  ├── Injection Risk        vulnerability to prompt injection attacks
  ├── Jailbreak Vulnerability susceptibility to adversarial safety bypass
  ├── Scope Drift Risk      unintended behavior change from prompt modifications
  └── Confidentiality Risk  system prompt exposure revealing proprietary logic

Workflow Risk
  ├── Orchestration Risk    multi-step workflows producing incorrect aggregates
  ├── External Dependency   risk from external API and service dependencies
  ├── Error Propagation     early-step errors amplifying through later steps
  └── Irreversibility Risk  degree to which workflow actions cannot be undone

Regulatory Risk
  ├── Explainability Gap    inability to explain decisions to regulatory standard
  ├── Documentation Deficit insufficient AI system documentation for examination
  ├── Jurisdictional Exposure operating in jurisdictions with uncertain AI law
  └── Data Privacy Exposure processing personal data creating regulatory liability
```

---

## Data Model

```yaml
RiskProfile:
  artifact_id: ArtifactRef
  risk_score:
    composite: float        # 0.0 – 10.0
    dimensions:
      agent_risk: float
      model_risk: float
      data_risk: float
      prompt_risk: float
      workflow_risk: float
      regulatory_risk: float
    confidence: float
    methodology: RiskMethodologyRef
  risk_tier: enum[Minimal, Low, Moderate, High, Critical]
  risk_factors: RiskFactor[]
  risk_mitigations: RiskMitigation[]
  risk_acceptance:            # nullable — present only if risk explicitly accepted
    accepted_by: PersonRef
    accepted_at: datetime
    rationale: string
    expires_at: datetime      # mandatory — unlimited acceptances prohibited
    conditions: string
  last_assessed: datetime
  next_review: datetime
  assessment_history: RiskAssessmentEvent[]

RiskFactor:
  factor_id: string
  domain: RiskDomain
  description: string
  weight: float
  value: float                # 0.0 – 10.0
  evidence: string
  mitigatable: boolean
```

---

## Risk Scoring Steps

1. **Factor Assessment**: Automated + human assessors assign 0–10 per risk factor from evidence
2. **Factor Weighting**: Tenant-configurable weights reflect firm's risk priorities
3. **Dimension Aggregation**: Weighted average per risk domain
4. **Composite Scoring**: Domains combined with amplification for highest-exposure areas
5. **Tier Classification**:
   - 0.0 – 2.0: Minimal → automated deployment
   - 2.1 – 4.0: Low → automated with monitoring
   - 4.1 – 6.0: Moderate → Tier 2 assisted review
   - 6.1 – 8.0: High → Tier 3 committee review
   - 8.1 – 10.0: Critical → deployment prohibited pending mitigation

---

## Services Exposed

| Method | Signature | SLA |
|--------|-----------|-----|
| ScoreRisk | `(artifact, context) → RiskProfile` | P99 < 500ms |
| GetRiskPosture | `(scope) → AggregateRiskPosture` | P99 < 1s |
| SetRiskThreshold | `(artifact_type, tier, threshold) → ThresholdConfig` | Async |
| RecordRiskAcceptance | `(artifact, acceptor, rationale, expiry) → AcceptanceRecord` | P99 < 200ms |
| GetRiskTrend | `(artifact, period) → RiskTrendReport` | Async |
| TriggerRiskReassessment | `(artifact, reason) → RiskAssessmentJob` | Async |

---

## Risk Reassessment Triggers

- Artifact configuration change (new model, prompt, tool)
- Evaluation regression detected
- Security incident involving artifact
- CVE or vulnerability affecting used model
- Regulatory change increasing jurisdictional exposure
- Risk acceptance record approaching expiry
- Behavioral monitoring anomaly detected
- Scheduled periodic review (frequency depends on risk tier)

---

## Extension Points

- Custom risk scoring algorithms per artifact type
- External risk data feeds (regulatory alerts, model vulnerability databases)
- New risk domains added to taxonomy without affecting existing scores
- Custom risk acceptance authority rules per tenant
