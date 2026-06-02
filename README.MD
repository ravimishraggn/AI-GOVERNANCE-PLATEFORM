# AI Governance Platform

Enterprise AI Governance Platform for Private Markets — Multi-Tenant SaaS

---

## What This Is

The AI Governance Platform is the trust infrastructure for the Private Markets AI Platform.
It governs every AI artifact — agents, models, prompts, datasets, knowledge assets, tools,
and workflows — deployed across 100+ product teams and hundreds of enterprise customers.

It answers the six enterprise questions no individual application team can answer alone:

1. Who authorized this AI decision, and when?
2. Which model produced this output, and what were its constraints?
3. Does this agent behavior comply with our regulatory obligations?
4. What risk did we accept when we deployed this workflow?
5. Can we reproduce this analysis from six months ago for an auditor?
6. Is this AI system behaving the same way today as it was when we certified it?

---

## Repository Structure

```
AI-GOVERNANCE-PLATFORM/
├── docs/                         # Architecture, decisions, roadmap documentation
│   ├── vision/                   # Why the platform exists
│   ├── architecture/             # Logical, physical, conceptual architecture
│   ├── control-planes/           # Deep-dive on each of the 8 control planes
│   ├── metadata-model/           # Governance metadata schemas for all artifact types
│   ├── multi-tenancy/            # Tenant isolation and policy inheritance
│   ├── compliance/               # Regulatory framework coverage
│   ├── risk-framework/           # Enterprise AI risk taxonomy and scoring
│   ├── operating-model/          # How product teams interact with governance
│   ├── roadmap/                  # Five-phase evolution roadmap
│   └── decisions/                # Architecture Decision Records (ADRs)
│
├── platform/                     # Platform services, SDKs, data models, events
│   ├── services/                 # 13 bounded governance microservices
│   ├── sdk/                      # Python and TypeScript Governance SDKs
│   ├── data-models/              # JSON schemas for all governance entities
│   └── events/                   # Event catalog and event schemas
│
├── governance/                   # Governance content: policies, risk, compliance
│   ├── policies/                 # Platform, regulatory, and template policies
│   ├── risk/                     # Risk taxonomy, scoring, and templates
│   ├── compliance/               # Compliance frameworks and control definitions
│   ├── manifests/                # Governance manifest templates and examples
│   ├── evaluation/               # Benchmarks, scorecards, and evaluation rubrics
│   └── workflows/                # Approval, certification, and incident workflows
│
├── tenants/                      # Tenant templates and onboarding guides
├── infrastructure/               # Kubernetes, Docker, data store schemas, monitoring
└── extensions/                   # Plugin contract interfaces and first-party plugins
```

---

## Quick Start for Product Teams

### Step 1: Register Your Artifact

Use the appropriate governance manifest template:

```
governance/manifests/templates/agent-manifest-template.yaml
governance/manifests/templates/model-manifest-template.yaml
governance/manifests/templates/prompt-manifest-template.yaml
governance/manifests/templates/workflow-manifest-template.yaml
```

See `governance/manifests/examples/` for complete worked examples.

### Step 2: Submit for Governance Clearance

```bash
governance-cli submit --manifest your-agent-manifest.yaml
# Returns: clearance status, risk tier, required actions, evaluation requirements
```

### Step 3: Embed the Governance SDK

```python
from governance_sdk import GovernanceClient, AgentSDK

client = GovernanceClient(artifact_id="your-agent-id")
sdk = AgentSDK(client)
response = await sdk.invoke(messages=messages, model="claude-sonnet-4-6")
```

### Step 4: Monitor Governance Posture

Access the Developer Portal to view risk profile, compliance posture,
evaluation scorecard, open approvals, and policy alerts.

---

## Platform Services

| Service                      | Port | Purpose                                  |
|------------------------------|------|------------------------------------------|
| governance-gateway           | 8000 | API routing, authentication, rate limits |
| policy-service               | 8001 | Policy storage, compilation, evaluation  |
| registry-service             | 8002 | Artifact registration and metadata       |
| audit-service                | 8003 | Immutable append-only audit log          |
| risk-service                 | 8004 | Risk scoring and threshold management    |
| compliance-service           | 8005 | Compliance posture tracking              |
| evaluation-service           | 8006 | Benchmark execution and scorecards       |
| approval-service             | 8007 | Approval workflow orchestration          |
| security-service             | 8008 | AI-specific security controls            |
| observability-service        | 8009 | Cost, latency, quality monitoring        |
| lineage-service              | 8010 | Lineage graph construction and query     |
| notification-service         | 8011 | Event-driven alerts and subscriptions    |
| tenant-management-service    | 8012 | Tenant provisioning and configuration    |

---

## Governance Tiers

| Tier   | Risk Score  | Process             | Deployment Time     |
|--------|-------------|---------------------|---------------------|
| Tier 1 | 0.0 – 4.0   | Automated clearance | Minutes             |
| Tier 2 | 4.1 – 6.0   | Assisted review     | 1–3 business days   |
| Tier 3 | 6.1 – 10.0  | Committee review    | 5–10 business days  |

---

## Key Documentation

- [Vision and Mission](docs/vision/vision-and-mission.md)
- [Architecture Overview](docs/architecture/logical-architecture.md)
- [Operating Model](docs/operating-model/self-service-model.md)
- [Policy Inheritance](docs/multi-tenancy/tenant-policy-inheritance.md)
- [Risk Framework](docs/risk-framework/risk-taxonomy.md)
- [Five-Year Roadmap](docs/roadmap/phase-1-foundation.md)
- [Python SDK](platform/sdk/python/README.md)
- [TypeScript SDK](platform/sdk/typescript/README.md)

---

## Governance Team Contacts

| Function            | Owns                                            |
|---------------------|-------------------------------------------------|
| Platform Engineering | Services, SDK, APIs, infrastructure            |
| Policy Team          | Policy content, policy lifecycle               |
| Risk Team            | Risk model, scoring, acceptance workflows      |
| Compliance Team      | Regulatory mapping, posture, evidence packages |
| Evaluation Team      | Benchmarks, evaluation infra, domain quality   |
