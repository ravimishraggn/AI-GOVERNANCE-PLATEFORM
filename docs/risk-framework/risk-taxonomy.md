# Enterprise AI Risk Taxonomy

## Risk Scoring Overview

Every registered AI artifact receives a multi-dimensional risk profile. Risk scores are:
- Computed automatically from declared artifact attributes and behavioral signals
- Updated whenever configuration, context, or behavior changes
- Used to determine approval tier, monitoring intensity, and certification requirements
- Retained in history for trend analysis and audit

Score range: 0.0 (no risk) to 10.0 (maximum risk)
Risk tier thresholds are configurable per tenant.

---

## Full Risk Taxonomy

### Domain 1: Agent Risk

| Factor | What It Measures | High-Score Indicators |
|--------|-----------------|----------------------|
| Autonomy Risk | Probability of unintended consequential actions | FullyAutonomous level, financial transaction tools |
| Escalation Risk | Probability of action chains beyond design | Deep tool chains, sub-agent orchestration |
| Tool Misuse Risk | Probability of harmful tool invocation | Write tools, irreversible tools, external API calls |
| Loop Risk | Probability of pathological execution | No circuit breaker, unbounded loops in design |
| Trust Propagation | Compromised agent spreading to network | Orchestrates other agents, elevated trust level |

### Domain 2: Model Risk

| Factor | What It Measures | High-Score Indicators |
|--------|-----------------|----------------------|
| Hallucination Risk | Tendency to generate false-but-plausible outputs | High benchmark hallucination rate, ungrounded domain |
| Bias Risk | Systematic unfair patterns in outputs | Known biases in training data for domain |
| Capability Boundary | Gap between apparent and reliable capabilities | Novel use case, outside training domain |
| Alignment Risk | Divergence from intended use optimization | Safety alignment not validated for this domain |
| Provider Dependency | Operational risk from single provider | Only one approved provider, no fallback |

### Domain 3: Data Risk

| Factor | What It Measures | High-Score Indicators |
|--------|-----------------|----------------------|
| Sensitivity Risk | Confidentiality of accessed data | Restricted/TopSecret classification |
| Leakage Risk | Probability of sensitive data in outputs | No output classification controls, external API calls |
| Poisoning Risk | Adversarial content corrupting behavior | External document ingestion, public RAG sources |
| Staleness Risk | Outdated data causing incorrect outputs | Data vintage > 6 months, rapidly changing domain |
| Lineage Risk | Inability to trace data origins | Missing source documentation, synthetic data |

### Domain 4: Prompt Risk

| Factor | What It Measures | High-Score Indicators |
|--------|-----------------|----------------------|
| Injection Risk | Vulnerability to prompt injection | User-controlled inputs in prompt, no injection controls |
| Jailbreak Vulnerability | Susceptibility to safety bypass | Novel prompt structure, limited safety evaluation |
| Scope Drift Risk | Unintended behavior from prompt changes | Frequent changes, no regression testing |
| Confidentiality Risk | System prompt exposure | Proprietary methodology in prompt, no prompt protection |

### Domain 5: Workflow Risk

| Factor | What It Measures | High-Score Indicators |
|--------|-----------------|----------------------|
| Orchestration Risk | Multi-step workflow producing incorrect aggregates | Complex orchestration, shared mutable state |
| External Dependency | Risk from external service dependencies | Multiple external APIs, no fallback strategy |
| Error Propagation | Early errors amplifying through later steps | No intermediate validation, cascading steps |
| Irreversibility Risk | Actions that cannot be undone | Financial transactions, database writes, email sends |

### Domain 6: Regulatory Risk

| Factor | What It Measures | High-Score Indicators |
|--------|-----------------|----------------------|
| Explainability Gap | Inability to explain decisions to required level | No lineage, black-box model, no audit trail |
| Documentation Deficit | Insufficient AI system documentation | Missing manifest fields, no evaluation evidence |
| Jurisdictional Exposure | Operating in uncertain regulatory environments | Multi-jurisdiction, evolving AI regulations |
| Privacy Exposure | Processing personal data creating liability | PII present, cross-border transfer, GDPR scope |

---

## Default Risk Weights

```yaml
# Default weights — configurable per tenant
risk_dimension_weights:
  agent_risk: 0.25
  model_risk: 0.20
  data_risk: 0.20
  prompt_risk: 0.15
  workflow_risk: 0.10
  regulatory_risk: 0.10

# Factor weights within agent_risk (example)
agent_risk_factor_weights:
  autonomy_risk: 0.30
  escalation_risk: 0.25
  tool_misuse_risk: 0.25
  loop_risk: 0.10
  trust_propagation_risk: 0.10
```

---

## Risk Tier Thresholds (Default)

| Tier | Score Range | Approval | Monitoring | Re-assessment |
|------|------------|----------|-----------|--------------|
| Minimal | 0.0 – 2.0 | Automated | Standard | Annual |
| Low | 2.1 – 4.0 | Automated + monitoring | Enhanced | Semi-annual |
| Moderate | 4.1 – 6.0 | Tier 2 review | High | Quarterly |
| High | 6.1 – 8.0 | Committee review | Intensive | Monthly |
| Critical | 8.1 – 10.0 | Deployment prohibited | N/A | N/A until mitigated |
