# Dataset Metadata Model

## Schema

```yaml
DatasetRecord:
  # Identity
  dataset_id: UUID
  canonical_name: string
  version: semver
  display_name: string
  description: string

  # Classification
  dataset_type: enum[Training, Evaluation, RAG, FineTuning, GroundTruth, Synthetic]
  domain: string
  sub_domain: string

  # Content Profile
  schema: DataSchema
  record_count: int64
  file_size_gb: float
  data_vintage:
    from_date: date
    to_date: date
  geographic_coverage: string[]
  asset_class_coverage: string[]   # PE, VC, Credit, Real Assets, etc.
  languages: string[]

  # Data Governance
  data_classification: enum[Public, Internal, Confidential, Restricted]
  pii_present: boolean
  pii_fields: string[]
  pii_handling_policy: PolicyRef
  data_lineage: LineageRef
  source_systems: DataSourceRef[]
  transformation_history: TransformationEvent[]

  # Legal and Compliance
  data_license: LicenseRef
  use_restrictions: string[]
  prohibited_uses: string[]
  retention_policy: RetentionPolicy
  applicable_regulations: RegulationRef[]
  cross_border_transfer_allowed: boolean

  # Quality
  quality_profile:
    completeness_score: float
    consistency_score: float
    accuracy_score: float
    timeliness_score: float
  last_quality_assessment: datetime
  known_issues: DataIssue[]

  # Access
  access_control: AccessControlList
  approved_consumers: ConsumerSpec[]   # which artifact types can use this dataset

  # Lifecycle
  status: enum[Active, Deprecated, Retired]
  refresh_schedule: cron_expression
  last_refreshed: datetime
  owner: TeamRef
```
