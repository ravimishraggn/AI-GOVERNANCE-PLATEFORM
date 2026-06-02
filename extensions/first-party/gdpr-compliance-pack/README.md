# GDPR Compliance Pack

First-party governance plugin for EU General Data Protection Regulation compliance.

## Covered Requirements

| Article | Requirement |
|---------|-------------|
| Article 5 | Data minimization and purpose limitation |
| Article 13/14 | Transparency: data subjects informed of automated processing |
| Article 17 | Right to erasure: AI systems must support erasure workflows |
| Article 22 | Automated decision-making rights and human oversight |
| Article 25 | Privacy by design: governance manifest privacy checks |
| Article 30 | Records of processing activities for AI systems |
| Article 35 | DPIA requirement for high-risk AI processing |

## Controls Provided

- GDPR applicability determination based on tenant profile and data flows
- Article 22 compliance check (human oversight for significant automated decisions)
- Data minimization policy enforcement (no more data than necessary for the task)
- Consent tracking integration for personal data processing
- Right-to-erasure workflow trigger for AI training data
- DPIA requirement flagging for high-risk AI deployments
- Cross-border transfer restriction enforcement

## Activation

```bash
governance-cli plugins activate gdpr-compliance-pack \
  --tenant your-tenant-id \
  --data-residency-regions [eu-west-1, eu-central-1]
```

Requires DPO (Data Protection Officer) authorization.
