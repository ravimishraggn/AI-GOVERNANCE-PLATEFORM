# Compliance Service

## Purpose

Maps regulatory obligations to platform controls, tracks compliance posture continuously,
and generates evidence for regulatory reporting and examinations.

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/compliance/posture/{tenant_id}` | Get compliance posture for tenant |
| GET | `/v1/compliance/posture/{tenant_id}/{framework_id}` | Posture for specific framework |
| POST | `/v1/compliance/evidence` | Generate evidence package |
| GET | `/v1/compliance/frameworks` | List available frameworks |
| GET | `/v1/compliance/frameworks/{framework_id}` | Get framework details |
| POST | `/v1/compliance/exceptions` | Register compliance exception |
| GET | `/v1/compliance/exceptions/{tenant_id}` | List active exceptions |
| POST | `/v1/compliance/assess-impact` | Assess impact of regulatory change |
| GET | `/v1/compliance/gaps/{tenant_id}` | Get open compliance gaps |

## Covered Frameworks

See [docs/control-planes/compliance-plane.md](../../../docs/control-planes/compliance-plane.md)
for the full list of supported regulatory frameworks.

## Evidence Package Generation

Evidence packages are generated as structured ZIP archives containing:
- Compliance posture summary with control-by-control status
- Policy evaluation records showing platform controls in operation
- Audit event samples demonstrating control effectiveness
- Model registry extracts showing MRM-required documentation
- Approval workflow records for human oversight evidence
- Exception register with justification and authorization records
