# Tenant Metadata Model

## Schema

```yaml
TenantRecord:
  # Identity
  tenant_id: UUID
  canonical_name: string            # stable identifier
  display_name: string
  description: string

  # Classification
  tenant_type: enum[InternalTeam, EnterpriseCustomer, ResearchPartner, TrialCustomer]
  industry: string                  # e.g., "Private Equity", "Venture Capital"
  firm_type: string                 # e.g., "Fund Manager", "Investment Bank"
  employee_count_band: string       # for risk calibration
  aum_band: string                  # AUM band for regulatory threshold determination

  # Regulatory Profile
  regulatory_profile:
    jurisdictions: string[]         # e.g., [US, EU, UK, Singapore]
    sec_registered_adviser: boolean
    finra_member: boolean
    aifmd_scope: boolean
    gdpr_applicable: boolean
    applicable_frameworks: ComplianceFrameworkRef[]

  # Governance Configuration
  policy_set: PolicySetRef          # tenant-specific policies (extends platform baseline)
  risk_tolerance:
    default_threshold_tier: RiskTierThreshold
    dimension_weights: Map<RiskDomain, float>
    acceptance_authority:
      low_risk: string              # "team_lead"
      moderate_risk: string         # "governance_team"
      high_risk: string             # "cro"
      critical_risk: string         # "executive_committee"
  approval_workflow_config: ApprovalWorkflowConfig

  # Data Sovereignty
  data_residency_requirements:
    allowed_regions: string[]
    prohibited_regions: string[]
    data_localization_required: boolean
  isolation_tier: enum[Logical, Namespace, Dedicated]

  # Commercial
  subscription_tier: enum[Starter, Professional, Enterprise, Dedicated]
  allocated_quotas:
    monthly_token_budget: int64
    max_agents: int
    max_workflows: int
    max_concurrent_executions: int
  cost_center: string
  billing_contact: PersonRef

  # Security
  encryption_config:
    key_management: enum[PlatformManaged, CustomerManaged, HSM]
    encryption_at_rest: boolean
    encryption_in_transit: boolean
  allowed_model_providers: ProviderRef[]
  allowed_data_classifications: string[]

  # Contacts
  governance_contacts:
    primary: PersonRef
    compliance: PersonRef
    security: PersonRef
    technical: PersonRef

  # Lifecycle
  status: enum[Onboarding, Active, Suspended, Offboarding, Terminated]
  onboarded_at: datetime
  last_governance_review: datetime
  next_governance_review: datetime
```
