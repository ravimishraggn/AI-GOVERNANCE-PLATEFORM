# Approval Service

## Purpose

Orchestrates human review workflows for governance decisions that cannot be automated.
Routes requests to appropriate reviewers, tracks state, enforces SLAs, and records decisions.

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/approvals/submit` | Submit approval request |
| GET | `/v1/approvals/{request_id}` | Get request status |
| GET | `/v1/approvals/pending` | Get pending reviews for caller |
| POST | `/v1/approvals/{request_id}/decide` | Submit approval decision |
| POST | `/v1/approvals/{request_id}/escalate` | Escalate request |
| POST | `/v1/approvals/{request_id}/withdraw` | Withdraw request |
| GET | `/v1/workflows` | List workflow templates |
| POST | `/v1/workflows` | Create workflow template (admin) |
| GET | `/v1/metrics` | Approval workflow metrics |

## Workflow Templates

Pre-configured templates determine routing and SLA based on artifact type and risk tier.
Templates are configurable per tenant via the tenant management service.

Default templates:
- `tier-1-auto` — automated clearance for low-risk artifacts
- `tier-2-assisted` — single governance reviewer + team lead
- `tier-3-committee` — Risk + Compliance + Security sign-off

See [governance/workflows/approval/](../../../governance/workflows/approval/) for YAML definitions.

## SLA Policy

| Tier | SLA | Escalation | Override |
|------|-----|-----------|---------|
| Tier 1 | 5 minutes | Automated | N/A |
| Tier 2 | 2 business days | At 100% SLA → next level | Risk manager |
| Tier 3 | 10 business days | At 100% SLA → executive | CAIO |

Expired requests are automatically rejected and require resubmission.
