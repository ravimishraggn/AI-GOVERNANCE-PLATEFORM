# Evaluation Plane

## Purpose

The Evaluation Plane provides institutional infrastructure for systematically measuring the
quality, safety, and reliability of every AI artifact through repeatable, versioned
evaluations that gate deployment and monitor production behavior.

---

## Evaluation Types

### Offline Evaluation (Pre-Deployment)
Systematic measurement against fixed, versioned datasets and benchmarks before any
deployment. Answers: "Is this artifact ready for production?"

Key benchmark categories:
- **Factual Accuracy**: Against ground-truth Q&A pairs from the domain
- **Hallucination Rate**: Against fact-checking benchmarks, red-team datasets
- **Safety**: Against adversarial prompt sets and safety evaluation suites
- **Instruction Following**: Against structured test cases for prompt fidelity
- **Domain Performance**: Private markets specific: valuation accuracy, credit quality
- **Robustness**: Performance under adversarial inputs and distribution shift

### Online Evaluation (Production Monitoring)
Continuous measurement of production artifacts against behavioral signals.
Answers: "Is this artifact continuing to behave correctly in production?"

Signals:
- Production hallucination rate (LLM-as-judge, reference-based)
- Response latency distribution vs. certified baseline
- User feedback signals (corrections, regeneration requests, thumbs)
- Retrieval quality for RAG applications
- Tool call success rate for agentic applications

### Human Evaluation
Qualitative dimensions that cannot be automated:
- Qualitative accuracy: Would a domain expert agree?
- Appropriateness: Correct for audience and context?
- Completeness: All relevant aspects addressed?
- Domain correctness: Private markets professional-level quality?

---

## Data Model

```yaml
EvaluationBenchmark:
  id: UUID
  name: string
  domain: enum[Safety, Quality, Accuracy, Latency, Cost, Compliance, Hallucination]
  methodology: EvaluationMethodology
  dataset: EvaluationDatasetRef
  metrics: MetricSpec[]
  passing_thresholds:
    accuracy: float           # e.g., 0.85 minimum
    hallucination_rate: float # e.g., 0.02 maximum
    safety_score: float       # e.g., 0.95 minimum
  version: semver
  applicable_to: ArtifactCriteria
  owner: TeamRef
  last_validated: datetime

EvaluationResult:
  id: UUID
  artifact: ArtifactRef
  artifact_version: semver
  benchmark: BenchmarkRef
  run_timestamp: datetime
  scores:
    per_metric: Map<string, float>
    aggregate: float
  pass_fail: enum[Pass, Fail, Conditional]
  regression_detected: boolean
  baseline_comparison:
    baseline_version: semver
    delta_per_metric: Map<string, float>
    regression_severity: enum[None, Minor, Major, Critical]
  evaluator_type: enum[Automated, Human, Hybrid]
  evidence: EvaluationEvidenceRef

EvaluationScorecard:
  artifact: ArtifactRef
  evaluation_date: datetime
  benchmarks_run: BenchmarkRef[]
  overall_score: float
  dimension_scores:
    safety: float
    quality: float
    accuracy: float
    domain_performance: float
  pass_fail_summary:
    passed: int
    failed: int
    conditional: int
  regression_alerts: RegressionAlert[]
  human_review_notes: string
  certification_eligible: boolean
  certification_conditions: string[]
```

---

## Evaluation Governance Integration

**Evaluation gates deployment**: Approval Plane requires evaluation clearance. An artifact
with failing benchmarks cannot advance through the approval workflow.

**Evaluation drives risk scores**: Poor evaluation outcomes increase risk scores.
A hallucination rate above threshold increases the artifact's Hallucination Risk factor.

**Evaluation evidence feeds compliance**: Scorecards become part of the compliance evidence
package for regulations requiring AI validation documentation (SR 11-7).

**Evaluation history supports audit**: Complete evaluation history available for audit queries
supporting "was this system validated before deployment?"

---

## Services Exposed

| Method | Signature | SLA |
|--------|-----------|-----|
| RunEvaluation | `(artifact, benchmark) → EvaluationJob` | Async |
| GetEvaluationScorecard | `(artifact, version) → Scorecard` | P99 < 500ms |
| RegisterBenchmark | `(benchmark_spec) → Benchmark` | Async |
| GetEvaluationHistory | `(artifact) → EvaluationResult[]` | P99 < 500ms |
| DetectRegression | `(artifact, v_a, v_b) → RegressionReport` | Async |
| SubmitHumanEvaluation | `(artifact, evaluation) → HumanEvalRecord` | P99 < 200ms |
| GetBenchmarkLibrary | `(domain, artifact_type) → Benchmark[]` | P99 < 200ms |

---

## Domain-Specific Benchmarks (Private Markets)

| Benchmark | Measures | Dataset Source |
|-----------|---------|---------------|
| Valuation Accuracy | Accuracy of AI-assisted valuation vs. independent appraiser | Historical valuations |
| Credit Analysis Quality | Agreement with credit analyst decisions | Historical credit decisions |
| Financial Document Accuracy | Factual accuracy over financial statements | Annual reports, SEC filings |
| Regulatory Language Compliance | Outputs compliant with regulatory disclosure standards | Compliance-reviewed samples |
| Deal Summary Quality | Completeness and accuracy of deal summaries | Anonymized deal documents |

---

## Extension Points

- Custom evaluation metrics for domain-specific quality dimensions
- Integration with external benchmark suites (HELM, BIG-Bench, industry benchmarks)
- Custom human evaluation rubrics
- Production signal integration for online evaluation from external systems
