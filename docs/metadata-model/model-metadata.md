# Model Metadata Model

## Purpose

Model metadata is the foundation of Model Risk Management (MRM) compliance for AI.
SR 11-7 and equivalent frameworks require a complete, current inventory of every model
with full documentation of its capabilities, limitations, validation status, and risk.

---

## Complete Schema

```yaml
ModelRecord:
  # ── Identity ──────────────────────────────────────────────────
  model_id: UUID
  provider: ProviderRef             # anthropic, openai, google, cohere, internal
  model_family: string              # claude, gpt, gemini, etc.
  model_name: string                # claude-sonnet-4-6, gpt-4o, etc.
  version: string                   # provider version string
  platform_tier: enum[Foundation, FineTuned, Custom, Proprietary, Embedded]

  # ── Capability ────────────────────────────────────────────────
  modalities: enum[Text, Image, Audio, Video, Code, Multimodal][]
  context_window_tokens: int
  max_output_tokens: int
  supports_function_calling: boolean
  supports_streaming: boolean
  supports_vision: boolean
  supports_structured_output: boolean
  languages: string[]               # ISO language codes
  training_data_cutoff: date

  # ── Commercial ────────────────────────────────────────────────
  pricing_model:
    input_cost_per_1k_tokens: float   # USD
    output_cost_per_1k_tokens: float  # USD
    image_cost_per_unit: float        # USD, if applicable
  rate_limits:
    requests_per_minute: int
    tokens_per_minute: int
    requests_per_day: int
  provider_data_retention_policy:
    retains_prompts: boolean
    retention_period_days: int
    data_used_for_training: boolean
  terms_of_service_version: string
  terms_last_reviewed: date

  # ── Governance Classification ──────────────────────────────────
  model_risk_rating: enum[Low, Moderate, High, VeryHigh]
  known_biases:
    - bias_type: string
      description: string
      severity: enum[Low, Medium, High]
      source_reference: string
  safety_alignment:
    alignment_approach: string       # RLHF, Constitutional AI, etc.
    safety_evaluation_score: float
    red_team_conducted: boolean
    safety_card_url: string
  known_vulnerabilities: VulnerabilityRef[]

  # ── Approved / Prohibited Use ─────────────────────────────────
  approved_use_cases: string[]
  prohibited_use_cases: string[]
  # e.g., prohibited: ["Autonomous trading decisions without human review",
  #                    "Sole basis for credit decisions"]

  # ── Certification ──────────────────────────────────────────────
  mrm_certification:
    status: enum[Pending, UnderReview, Certified, ConditionalCertification,
                  Rejected, Expired]
    certified_by: PersonRef
    certified_at: datetime
    expires_at: datetime
    conditions: string[]
    certified_use_cases: string[]    # certification is use-case specific
  evaluation_history: EvaluationRef[]

  # ── Lifecycle ─────────────────────────────────────────────────
  platform_status: enum[UnderReview, Approved, Active, Deprecated, Retired]
  deprecated_at: date                # nullable
  deprecation_notice: string
  retirement_date: date              # nullable
  replacement_model: ModelRef        # nullable
  migration_guide: string
```

---

## Model Onboarding Process

```
Stage 1: Technical Assessment
  ├── API compatibility verification
  ├── Capability profiling (benchmarks, context window, rate limits)
  └── Pricing model documentation

Stage 2: Security Assessment
  ├── Provider data retention policy review
  ├── Terms of service review for data handling
  ├── Vulnerability assessment (known CVEs, security advisories)
  └── Data flow analysis (what leaves the platform boundary)

Stage 3: Risk Assessment
  ├── Model risk rating assignment
  ├── Hallucination benchmark evaluation on domain datasets
  ├── Bias assessment for private markets domain
  └── Alignment assessment for intended use cases

Stage 4: Compliance Review
  ├── Regulatory acceptability per applicable frameworks
  ├── Approved/prohibited use case definition
  └── Jurisdiction-specific restrictions documented

Stage 5: Commercial Review
  ├── Cost model analysis and volume pricing
  ├── SLA review and uptime commitments
  └── Vendor risk assessment (concentration risk)

Stage 6: MRM Certification
  └── Formal sign-off by Model Risk Management function
```

---

## Model Retirement Process

1. Deprecation announcement: 90-day notice minimum
2. All consuming agent owners notified via Notification Service
3. Migration guidance published with recommended replacement
4. Graduated enforcement: warnings for 60 days, then hard blocks
5. Hard cutoff: unregistered use of retired models blocked at platform level
6. Archival: retired model records preserved indefinitely for audit
