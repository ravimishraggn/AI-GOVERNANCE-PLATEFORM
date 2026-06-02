# Logical Architecture

## Overview

The Governance Platform is organized into five logical layers. Each layer has a clear
responsibility and depends only on layers below it.

```
┌──────────────────────────────────────────────────────────────────────┐
│                        CONSUMER LAYER                                │
│  Product Teams │ CI/CD Pipelines │ Developer Portal │ Auditors      │
│  External Tenants │ Compliance Officers │ Risk Managers             │
└──────────────────────────────────────────────────────────────────────┘
                                  │
                     ┌────────────▼───────────┐
                     │   GOVERNANCE API LAYER  │
                     │  REST │ GraphQL │ Events │
                     │   Governance Gateway    │
                     └────────────┬───────────┘
                                  │
┌─────────────────────────────────▼────────────────────────────────────┐
│                  GOVERNANCE CONTROL PLANE LAYER                      │
│                                                                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ Policy   │ │  Risk    │ │Compliance│ │ Security │ │  Audit   │ │
│  │ Plane    │ │  Plane   │ │  Plane   │ │  Plane   │ │  Plane   │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
│                                                                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────────┐                        │
│  │ Approval │ │Evaluation│ │Observability │                         │
│  │  Plane   │ │  Plane   │ │    Plane     │                         │
│  └──────────┘ └──────────┘ └──────────────┘                        │
└─────────────────────────────────┬────────────────────────────────────┘
                                  │
┌─────────────────────────────────▼────────────────────────────────────┐
│                  GOVERNANCE CORE SERVICES LAYER                      │
│                                                                      │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐           │
│  │ Registry  │ │ Metadata  │ │  Lineage  │ │Evaluation │           │
│  │ Service   │ │ Service   │ │  Service  │ │  Service  │           │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘           │
│                                                                      │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐           │
│  │ Workflow  │ │Notification│ │  Tenant  │ │Extension  │           │
│  │  Engine   │ │  Service  │ │ Manager  │ │ Registry  │           │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘           │
└─────────────────────────────────┬────────────────────────────────────┘
                                  │
┌─────────────────────────────────▼────────────────────────────────────┐
│                  GOVERNANCE DATA PLATFORM LAYER                      │
│                                                                      │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐           │
│  │Governance │ │Immutable  │ │Governance │ │Time-Series│           │
│  │Metadata   │ │Audit Log  │ │Graph DB   │ │Metrics    │           │
│  │Store      │ │(Append-   │ │(Lineage)  │ │(Telemetry)│           │
│  │           │ │ Only)     │ │           │ │           │           │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘           │
└─────────────────────────────────┬────────────────────────────────────┘
                                  │
┌─────────────────────────────────▼────────────────────────────────────┐
│               INTEGRATION AND EXTENSION LAYER                        │
│  LLM Provider Connectors │ Data Platform Connectors                  │
│  SIEM Integration │ Identity Provider │ External Risk Feeds          │
│  Plugin Registry │ GRC Platform Connectors                           │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Four Interlocking Systems

### The Registry System (What Exists)
Authoritative source of truth for every AI artifact — agents, models, prompts, datasets,
tools, workflows. Every artifact must be registered before it can access platform resources.
Answers: "What do we have and what state is it in?"

### The Policy System (What Is Allowed)
Every registered artifact is continuously evaluated against the applicable policy set.
Policies are versioned, inherited hierarchically, and enforced automatically.
Answers: "What rules apply here and does this artifact comply?"

### The Risk System (What We Are Exposed To)
Every artifact has a continuously maintained risk profile. Risk scores change as
configuration, behavior, and external context change.
Answers: "What could go wrong and how bad would it be?"

### The Evidence System (What Happened)
Every significant governance event is recorded as an immutable, cryptographically-chained
evidence artifact. Supports forensic reconstruction of any past governance state.
Answers: "What happened, when, and why?"

---

## Consistency Guarantee

The four systems are always consistent with each other through the **Governance Event Bus**:

- A Registry change → Evidence event → Policy re-evaluation → Risk re-assessment
- A Policy change → Evidence event → All affected artifacts re-evaluated → Risk updated
- A Risk change → Evidence event → Approval workflows triggered if threshold crossed
- A Security event → Evidence event → Risk updated → Compliance posture updated

No system can change state without producing an evidence event. The event bus is the
nervous system of the platform.
