# Observability Service

## Purpose

Platform-level AI observability: cost attribution, latency monitoring, quality drift
detection, agentic behavior monitoring, and enterprise dashboards.

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/telemetry` | Ingest telemetry event (high-throughput) |
| GET | `/v1/dashboards/{scope}` | Get operational dashboard |
| GET | `/v1/cost/attribution` | Get cost attribution report |
| GET | `/v1/cost/forecast` | Get cost forecast |
| POST | `/v1/alerts/budget` | Set budget alert |
| GET | `/v1/alerts/anomalies` | Get anomaly alerts |
| GET | `/v1/quality/trends` | Get quality trend data |
| GET | `/v1/latency/{artifact_id}` | Get latency report |
| GET | `/v1/agents/{agent_id}/behavior` | Get agent behavior metrics |

## Telemetry Ingest

`POST /v1/telemetry` accepts high-throughput event streams from the Governance SDK.
Events are buffered in-memory and flushed in micro-batches to the time-series store.

The SDK sends telemetry asynchronously — telemetry ingest must never block AI inference.

## Cost Attribution Hierarchy

Cost events are attributed at each level of the hierarchy:
Platform → Region → Tenant → Team → Application → Agent → Session → Call

This enables cost reports at any granularity, supporting chargeback to individual tenants
and budget governance at team level.

## Anomaly Detection

Anomaly detection runs on a 5-minute rolling window using configurable statistical models:
- Latency anomaly: P99 > 3x rolling 24h baseline
- Cost anomaly: hourly cost > 5x rolling 7-day hourly average
- Quality anomaly: hallucination rate > 2x rolling 24h baseline
- Behavior anomaly: agent tool call depth > 3x certified baseline
