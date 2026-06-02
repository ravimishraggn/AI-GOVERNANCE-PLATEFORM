# Lineage Service

## Purpose

Constructs and maintains the lineage graph connecting every AI output back to its inputs,
models, prompts, data sources, and governance decisions. Enables forensic traceability.

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/lineage/record` | Record a lineage event (async) |
| GET | `/v1/lineage/{output_id}` | Get lineage for a specific output |
| GET | `/v1/lineage/upstream/{artifact_id}` | Get all upstream dependencies |
| GET | `/v1/lineage/downstream/{artifact_id}` | Get all downstream consumers |
| POST | `/v1/lineage/impact` | Get impact of changing an artifact |
| GET | `/v1/lineage/path` | Find lineage path between two artifacts |

## Lineage Graph Structure

```
AI OUTPUT (output_id)
  └── produced_by → AGENT (version at execution time)
        ├── using_model → MODEL (version at execution time)
        ├── with_prompt → PROMPT (version at execution time)
        ├── accessing → KNOWLEDGE_SOURCE (version/vintage at access time)
        │     └── sourced_from → DATASET (version at ingestion time)
        ├── calling_tool → TOOL (version at call time)
        └── for_user → USER (authorization at execution time)
```

All lineage nodes record the **version at the time of execution**, not the current version.
This enables historical reconstruction regardless of subsequent changes.

## Use Cases

**Change Impact Analysis**: Before upgrading model X, query which agents use it,
which workflows those agents are in, and which outputs they produce.

**Root Cause Analysis**: Starting from an incorrect AI output, trace back through
the lineage graph to identify which data source, prompt version, or model version
was responsible.

**Regulatory Explainability**: Produce the complete provenance of a specific AI decision
for a regulatory examination.
