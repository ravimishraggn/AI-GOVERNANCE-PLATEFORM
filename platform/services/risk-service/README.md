# Risk Service

## Purpose

The Risk Service owns the enterprise AI risk model, scores every registered artifact,
tracks risk posture over time, and enforces risk-based deployment gates.

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/risk/score` | Score an artifact's risk profile |
| GET | `/v1/risk/profiles/{artifact_id}` | Get current risk profile |
| GET | `/v1/risk/profiles/{artifact_id}/history` | Get risk score history |
| GET | `/v1/risk/posture` | Get aggregate risk posture (by scope) |
| PUT | `/v1/risk/thresholds` | Configure risk thresholds (admin) |
| POST | `/v1/risk/acceptance` | Record risk acceptance decision |
| GET | `/v1/risk/acceptance/{artifact_id}` | Get active risk acceptance |
| POST | `/v1/risk/reassess` | Trigger immediate risk reassessment |
| GET | `/v1/risk/trends` | Get risk trend report |

## Risk Reassessment Triggers

The risk service subscribes to the Governance Event Bus and automatically triggers
reassessment when:
- Artifact configuration changes (registry update event)
- Evaluation results change (evaluation complete event)
- Security incident involving the artifact (security event)
- Behavioral monitoring anomaly detected (observability alert event)
- Risk acceptance record expires (scheduled)
- Regulatory change event received (compliance event)

## Configuration

See [config/config.yaml](config/config.yaml) for risk model configuration,
including default factor weights and tier thresholds.
