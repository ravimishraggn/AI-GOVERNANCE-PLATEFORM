# ADR-004: Plugin-Based Extensibility Architecture

**Status:** Accepted
**Date:** 2026-05-31

## Decision

Implement a plugin bus architecture for governance extensibility. The core platform
defines stable extension points and contracts. Plugins implement contracts and register
with the Extension Registry. The platform routes to registered plugins at extension points.

## Extension Points Defined (Phase 3+)

| Extension Point | Purpose |
|----------------|---------|
| PolicyRule | Custom policy rule evaluators |
| RiskScorer | Custom risk scoring algorithms |
| ComplianceControl | Regulatory framework modules |
| EvaluationMetric | Custom evaluation benchmarks |
| AuditTransformer | Audit event transformations for external systems |
| ContentClassifier | Custom content classification models |
| WorkflowStep | Custom workflow step types |

## Plugin Isolation Requirements

Plugins run in sandboxed execution contexts. They cannot:
- Access platform internals or other tenants' data
- Make network calls not declared in their plugin manifest
- Consume unlimited compute resources
- Modify audit records

All plugin invocations are audited with the plugin identity recorded.

## Rationale

The AI governance landscape evolves faster than the platform can be rebuilt. New
regulations, new model types, new risk categories, and new evaluation methodologies
will emerge continuously. Without extensibility, the platform requires a redesign for
every new governance requirement. With extensibility, new requirements are satisfied
by adding a plugin without touching the platform core.
