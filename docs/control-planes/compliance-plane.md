# Compliance Plane

## Purpose

The Compliance Plane maps the enterprise's regulatory obligations and internal control
requirements to specific governance controls on the AI platform, tracks compliance posture
continuously, and generates evidence for regulatory reporting and audit.

---

## Responsibilities

- Maintain a library of applicable regulatory frameworks (SEC, FINRA, GDPR, AIFMD, etc.)
- Map regulatory requirements to specific platform controls, policies, and governance actions
- Track compliance posture for each tenant and AI artifact against applicable frameworks
- Generate compliance attestations, control evidence packages, and regulatory reports
- Alert on compliance posture degradation before it becomes a regulatory finding
- Manage compliance exceptions: who granted what exception, when, and when it expires
- Monitor the regulatory environment for new requirements and assess impact on deployments

---

## Data Model

```yaml
ComplianceFramework:
  id: UUID
  name: string              # e.g., "SEC SR 11-7", "GDPR Article 22"
  jurisdiction: string
  category: enum[ModelRisk, DataPrivacy, InvestmentAdvisory, FundManagement, AIAct]
  applicable_to: TenantCriteria
  requirements: ComplianceRequirement[]
  control_mapping: ControlMapping[]
  effective_date: date
  review_cycle: duration    # how often framework mapping is reviewed

CompliancePosture:
  tenant_id: TenantRef
  framework_id: FrameworkRef
  overall_status: enum[Compliant, NonCompliant, AtRisk, Exempt, UnderReview]
  control_statuses: ControlStatus[]
  open_gaps: ComplianceGap[]
  exceptions: ComplianceException[]
  last_assessed: datetime
  next_review: datetime
  evidence_packages: EvidencePackageRef[]

ComplianceException:
  exception_id: UUID
  requirement_id: RequirementRef
  granted_by: PersonRef
  granted_at: datetime
  rationale: string
  expires_at: datetime      # mandatory — unlimited exceptions prohibited
  conditions: string
  artifact_scope: ArtifactRef[]
```

---

## Covered Regulatory Frameworks

### Financial Services
| Framework | Jurisdiction | Primary Requirements |
|-----------|-------------|---------------------|
| SR 11-7 / OCC 2011-12 | US | Model risk management, validation, inventory |
| SEC Rule 17a-4 | US | Books and records, immutability |
| FINRA Rule 4511 | US | Record retention for member firms |
| MiFID II Article 17 | EU | Algorithmic trading governance, testing |
| AIFMD Article 18 | EU | Risk management for alternative fund managers |
| SEC Reg BI | US | Best interest standard for investment advice |

### Data Privacy
| Framework | Jurisdiction | Primary Requirements |
|-----------|-------------|---------------------|
| GDPR Article 22 | EU | Automated decision-making rights, explainability |
| GDPR Article 5 | EU | Data minimization, purpose limitation |
| CCPA / CPRA | California | Consumer rights, automated decision disclosures |
| NYC Local Law 144 | New York City | Automated employment decision tool auditing |

### Private Markets Specific
| Requirement | Source | Application |
|-------------|--------|-------------|
| Valuation independence | AIFMD, ILPA | AI-assisted valuation systems |
| MNPI controls | SEC Rule 10b-5 | Information barriers for AI with deal flow data |
| ERISA fiduciary | ERISA Section 404 | AI-assisted decisions for pension fund managers |

---

## Services Exposed

| Method | Signature | SLA |
|--------|-----------|-----|
| GetCompliancePosture | `(tenant, framework) → CompliancePosture` | P99 < 500ms |
| GenerateEvidencePackage | `(tenant, framework, period) → EvidencePackage` | Async |
| RegisterComplianceException | `(artifact, req, rationale, approver) → ExceptionRecord` | P99 < 200ms |
| GetApplicableFrameworks | `(tenant_profile) → ComplianceFramework[]` | P99 < 200ms |
| AssessControlCoverage | `(control) → CoverageReport` | Async |
| SubscribeToRegulatoryAlerts | `(criteria) → AlertSubscription` | Async |
| AssessRegulatoryImpact | `(new_regulation) → ImpactReport` | Async |

---

## Compliance Posture Dashboard Signals

- Green: All controls mapped, evidence complete, no open gaps
- Yellow (At Risk): Open gaps with remediation plans, or framework coverage < 90%
- Red (Non-Compliant): Open gaps without remediation plans, or missing evidence
- Grey (Exempt): Tenant profile excludes this framework

---

## Extension Points

- New regulatory framework modules added without platform redesign
- Custom control definitions for internal enterprise policies
- Integration hooks for external GRC platforms (ServiceNow, Archer, IBM OpenPages)
- Custom evidence package formats for specific regulatory requirements
