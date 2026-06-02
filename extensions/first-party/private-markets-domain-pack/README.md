# Private Markets Domain Pack

First-party governance plugin providing domain-specific evaluation benchmarks,
risk scoring factors, and compliance controls for private markets AI applications.

## What This Pack Provides

### Domain Evaluation Benchmarks
- `BENCH-DOMAIN-PM-001` — Private Markets Accuracy (see governance/evaluation/benchmarks/domain/)
- `BENCH-DOMAIN-VAL-001` — Valuation Methodology Accuracy
- `BENCH-DOMAIN-CREDIT-001` — Credit Analysis Quality
- `BENCH-DOMAIN-DEAL-001` — Deal Summary Completeness
- `BENCH-DOMAIN-REG-001` — Regulatory Language Compliance

### Domain Risk Factors
Custom risk factors specific to private markets AI:
- `MNPI_exposure_risk` — elevated risk for systems with deal flow access
- `valuation_methodology_risk` — risk for AIFMD-governed valuation systems
- `lp_communication_risk` — risk for AI-generated LP communications
- `regulatory_filing_risk` — risk for systems that assist in regulatory filings

### Domain Compliance Controls
- AIFMD Article 19 valuation independence controls
- ILPA (Institutional Limited Partners Association) reporting standards
- ERISA fiduciary duty documentation requirements for pension fund managers
- Carried interest and fee calculation audit requirements

### Private Markets Policy Templates
Pre-built governance manifest templates for:
- Private equity fund management agents
- Venture capital research agents
- Credit underwriting copilots
- Real assets valuation agents
- Fund administration workflows

## Activation

```bash
governance-cli plugins activate private-markets-domain-pack \
  --tenant your-tenant-id
```

Available to all tenants with `industry: Private Equity/VC/Credit/Real Assets`.
