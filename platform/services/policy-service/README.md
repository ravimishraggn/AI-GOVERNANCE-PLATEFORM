# Policy Service

## Purpose

The Policy Service is the authoritative engine for governance policy storage, compilation,
and evaluation. It is on the critical path of every AI inference request.

## Responsibilities

- Store the complete versioned library of governance policies
- Compile policies into evaluation-ready decision trees (optimized for low-latency evaluation)
- Distribute compiled policy decisions to tenant-local caches
- Evaluate incoming requests against applicable policy sets
- Detect and resolve policy conflicts
- Maintain full version history with change attribution
- Support policy inheritance hierarchy across platform, regulatory, tenant, team levels

## API Reference

See [api-spec/openapi.yaml](api-spec/openapi.yaml) for the full OpenAPI specification.

### Key Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/policies/evaluate` | Evaluate artifact against applicable policies |
| GET | `/v1/policies/{policy_id}` | Get a specific policy |
| GET | `/v1/policies` | List applicable policies by criteria |
| POST | `/v1/policies` | Create a new policy (governance team only) |
| PUT | `/v1/policies/{policy_id}/versions` | Publish a new policy version |
| GET | `/v1/policies/{policy_id}/history` | Get policy change history |
| POST | `/v1/policies/simulate` | Simulate policy impact before publishing |
| GET | `/v1/policies/conflicts` | Get active policy conflicts |

## Performance Requirements

| Operation | P50 | P99 |
|-----------|-----|-----|
| Evaluate (cache hit) | < 1ms | < 2ms |
| Evaluate (cache miss) | < 5ms | < 10ms |
| Get policy | < 20ms | < 50ms |
| Simulate impact | < 5s | < 30s |

## Policy Evaluation Flow

1. Resolve tenant context from request
2. Load applicable policy set (from cache if available)
3. For each applicable policy, evaluate conditions against artifact context
4. Resolve any conflicts using configured strategy
5. Return composite decision with policy IDs and justification

## Caching Strategy

- Compiled policy decisions cached in Redis per (artifact_type, tenant_id, context_hash)
- Cache invalidated on any policy change affecting the cached context
- Cache TTL: 5 minutes (failsafe expiry)
- Cold start: policies pre-compiled at service startup per active tenant
