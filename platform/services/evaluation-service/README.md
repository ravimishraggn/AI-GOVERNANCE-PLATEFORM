# Evaluation Service

## Purpose

Provides institutional infrastructure for systematically measuring the quality, safety,
and reliability of every AI artifact through repeatable, versioned evaluations.

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/evaluations/run` | Submit evaluation job |
| GET | `/v1/evaluations/{job_id}` | Get evaluation job status |
| GET | `/v1/evaluations/{job_id}/results` | Get evaluation results |
| GET | `/v1/scorecards/{artifact_id}` | Get latest scorecard |
| GET | `/v1/scorecards/{artifact_id}/history` | Get scorecard history |
| POST | `/v1/scorecards/{artifact_id}/compare` | Compare two versions |
| GET | `/v1/benchmarks` | List available benchmarks |
| POST | `/v1/benchmarks` | Register new benchmark |
| GET | `/v1/benchmarks/{benchmark_id}` | Get benchmark details |
| POST | `/v1/human-evaluations` | Submit human evaluation |
| GET | `/v1/regressions/{artifact_id}` | Get regression report |

## Evaluation Pipeline

```
SUBMIT (artifact_id, benchmark_ids)
  │
  ├── Load artifact configuration from Registry Service
  ├── Load benchmark specifications
  ├── Prepare evaluation dataset (versioned snapshot)
  │
  ├── For each benchmark:
  │   ├── Execute evaluation runs (parallelized)
  │   ├── Score against benchmark metrics
  │   ├── Compare to baseline (previous version or certified baseline)
  │   └── Detect regressions
  │
  ├── Generate scorecard
  ├── Update risk profile (evaluation results feed risk scores)
  ├── Notify relevant stakeholders if regression detected
  └── Return job_id for async status polling
```

## Regression Detection

A regression is detected when:
- Any metric score drops more than the configured threshold from the certified baseline
- A previously passing benchmark now fails
- Safety scores drop below the certified minimum

Regression severity:
- Minor: < 10% relative drop on non-safety metrics
- Major: > 10% relative drop, or any safety metric drop
- Critical: Safety benchmark failure

Critical regressions trigger an automated governance hold: the artifact cannot be
deployed until the regression is investigated and resolved.
