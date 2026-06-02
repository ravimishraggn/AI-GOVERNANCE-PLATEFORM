# Security Service

## Purpose

Enforces AI-specific security controls: prompt injection detection, data exfiltration
monitoring, jailbreak detection, and model abuse prevention.

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/security/evaluate` | Evaluate request security context (inline) |
| POST | `/v1/security/classify` | Classify content sensitivity |
| POST | `/v1/security/events` | Log security event |
| GET | `/v1/security/events` | Query security events |
| GET | `/v1/security/profiles/{artifact_id}` | Get security profile |
| POST | `/v1/security/assess` | Run security assessment on artifact |
| GET | `/v1/security/rules` | List active detection rules |
| POST | `/v1/security/rules` | Add custom detection rule (admin) |

## Inline Evaluation

`POST /v1/security/evaluate` is called inline for every AI inference request.
It must complete in < 5ms (P99). The evaluation:

1. Checks prompt content against injection detection model
2. Checks for known jailbreak patterns in the input
3. Classifies data sensitivity of the request context
4. Evaluates against active security rules for the tenant
5. Returns allow/block/flag decision with reason codes

## Detection Rule Configuration

Detection rules are configurable per tenant through the security service admin API.
Tenant rules are added on top of (not instead of) platform-level detection rules.

See [governance/policies/platform/safety/](../../../governance/policies/platform/safety/)
for base platform security policies.
