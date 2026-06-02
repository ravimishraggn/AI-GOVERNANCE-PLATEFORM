# Physical Architecture

## Non-Functional Requirements Driving Physical Design

| Requirement | Target | Rationale |
|-------------|--------|-----------|
| Inline policy evaluation latency | P50 < 2ms, P99 < 10ms | On critical path of AI inference |
| Governance platform availability | 99.999% (5 nines) | Platform-of-platforms dependency |
| Audit log durability | 99.9999999% (11 nines) | Regulatory evidence, no data loss |
| Tenant data isolation | Zero-tolerance cross-tenant | Regulatory, contractual, security |
| Multi-region support | US-EAST, EU-WEST minimum | Data residency requirements |

---

## Tiered Isolation Model

```
                  GLOBAL GOVERNANCE CONTROL PLANE
                  ┌──────────────────────────────┐
                  │  Global Policy Registry      │
                  │  Global Compliance Registry  │
                  │  Global Risk Model Registry  │
                  │  Global Evaluation Benchmarks│
                  │  Cross-Tenant Analytics      │
                  └──────────────────────────────┘
                         │              │
         ┌───────────────┘              └──────────────┐
         ▼                                             ▼
REGION: US-EAST                              REGION: EU-WEST
┌────────────────────┐                  ┌────────────────────┐
│ Regional Gov Plane │                  │ Regional Gov Plane │
│  Policy Cache      │                  │  Policy Cache      │
│  Audit Log Primary │                  │  Audit Log Primary │
│  Tenant Data Stores│                  │  Tenant Data Stores│
│  Inline Policy Svc │                  │  Inline Policy Svc │
└────────────────────┘                  └────────────────────┘
         │                                             │
 ┌───────▼──────┐                           ┌─────────▼────┐
 │ TENANT CELLS │                           │ TENANT CELLS │
 │ ┌──────────┐ │                           │ ┌──────────┐ │
 │ │ Tenant A │ │                           │ │ Tenant C │ │
 │ │Gov Store │ │                           │ │Gov Store │ │
 │ └──────────┘ │                           │ └──────────┘ │
 │ ┌──────────┐ │                           │ ┌──────────┐ │
 │ │ Tenant B │ │                           │ │ Tenant D │ │
 │ │Gov Store │ │                           │ │Gov Store │ │
 │ └──────────┘ │                           │ └──────────┘ │
 └──────────────┘                           └──────────────┘
```

---

## Isolation Tiers

### Tier 1: Logical Isolation (Default)
- Shared physical infrastructure
- Row-level security in all data stores, scoped to tenant cryptographic identity
- Tenant governance data encrypted with tenant-specific keys (stored in tenant-controlled KMS)
- No administrative path to cross-tenant data access
- Cost: lowest. Suitable for: internal teams, standard enterprise customers

### Tier 2: Namespace Isolation (Mid-Tier)
- Dedicated namespaces in shared infrastructure
- Physically separate data store instances per tenant
- Dedicated processing queues and audit log storage
- Governance control plane shared; all data planes isolated
- Cost: moderate. Suitable for: regulated customers, customers handling MNPI

### Tier 3: Dedicated Isolation (Premium)
- Dedicated governance infrastructure in tenant-controlled network segment
- Platform manages deployment and lifecycle; infrastructure is physically separate
- Customer controls encryption keys; platform cannot access data without customer authorization
- Cost: highest. Suitable for: large institutional investors with their own regulatory obligations

---

## Policy Evaluation Physical Flow

```
APPLICATION (in-process Governance SDK)
    │
    │ 1. Check local compiled policy cache (< 1ms)
    ├──[HIT, ALLOW]──► proceed to LLM, emit async audit event
    │
    │ 2. Cache miss: call nearest Regional Policy Service (< 5ms)
    ▼
REGIONAL POLICY SERVICE (same-region, edge-deployed)
    │
    │ 3. Evaluate against tenant policy set + platform baseline
    │ 4. Return allow/deny/warn + policy decision ID
    ▼
APPLICATION SDK
    │
    ├──[DENY]──► block call, emit audit event with decision ID
    ├──[WARN]──► allow with warning, emit audit event
    └──[ALLOW]──► proceed, emit async audit event
                       │
                       ▼ (async, non-blocking)
               REGIONAL AUDIT SERVICE
               (append-only, replicated to global)
```

---

## Data Store Assignments

| Data | Store Type | Isolation | Retention |
|------|-----------|-----------|-----------|
| Governance metadata | Relational (PostgreSQL) | Per-tenant schema | Indefinite |
| Audit log | Append-only columnar (S3 + Athena) | Per-tenant bucket | Per regulation |
| Lineage graph | Graph DB (Neo4j / Amazon Neptune) | Per-tenant graph | 7 years |
| Telemetry metrics | Time-series (InfluxDB / TimestreamDB) | Per-tenant namespace | 2 years hot |
| Policy compiled cache | In-memory (Redis) | Per-tenant keyspace | TTL-based |
| Evaluation results | Object store (S3) | Per-tenant prefix | 5 years |
