# Registry Service

## Purpose

The Registry Service is the authoritative source of record for every AI artifact on the
platform. Every agent, model, prompt, dataset, tool, knowledge asset, and workflow must
be registered here before it can receive platform services.

## Responsibilities

- Accept and validate artifact registration requests with governance manifests
- Assign stable governance identities (artifact_id) to all registered artifacts
- Maintain complete metadata records for all artifacts
- Track artifact lifecycle status from Development through Retirement
- Trigger downstream governance workflows on registration (risk assessment, evaluation, approval)
- Serve artifact metadata to all consuming services
- Enforce registration as a gateway to platform resource access

## Registration Enforcement

Registration is self-enforcing through platform dependency. An unregistered artifact cannot:
- Receive LLM API credentials through the platform
- Access platform-managed knowledge bases
- Have its calls governed by the Policy Service
- Generate compliant audit trails

This makes governance the path of least resistance, not an obstacle.

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/artifacts` | Register a new artifact |
| GET | `/v1/artifacts/{artifact_id}` | Get artifact record |
| PUT | `/v1/artifacts/{artifact_id}` | Update artifact metadata |
| POST | `/v1/artifacts/{artifact_id}/versions` | Register new version |
| GET | `/v1/artifacts/{artifact_id}/versions` | List all versions |
| GET | `/v1/artifacts/{artifact_id}/status` | Get governance status |
| POST | `/v1/artifacts/{artifact_id}/retire` | Initiate retirement |
| GET | `/v1/artifacts` | Search artifact registry |

## Artifact Status Lifecycle

```
DEVELOPMENT → STAGING → CERTIFICATION_REVIEW → CERTIFIED → PRODUCTION
     ↑                                                          │
     └──────────────── DEPRECATED ←───────────────────────────┘
                            │
                         RETIRED
```
