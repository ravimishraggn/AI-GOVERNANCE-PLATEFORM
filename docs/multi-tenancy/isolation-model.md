# Tenant Isolation Model

## Isolation Tiers

### Tier 1: Logical Isolation (Default for internal teams and standard customers)

Architecture:
- Shared physical infrastructure across all Tier 1 tenants
- Row-level security (RLS) in all database tables scoped to tenant_id
- All queries automatically filtered by tenant context from JWT/session
- Tenant governance data encrypted with tenant-specific symmetric keys
- Keys stored in platform KMS with tenant-scoped access policies
- Event streams partitioned by tenant_id with separate consumer groups

Security guarantee: Cross-tenant data access is architecturally impossible.
A query for Tenant A's audit events cannot return Tenant B's events even if the
application has a bug, because the encrypted keys are different and the RLS policies
enforce tenant isolation at the database engine level.

### Tier 2: Namespace Isolation (For regulated customers and MNPI handlers)

Architecture:
- Separate database schemas or instances per tenant
- Dedicated message queue topics per tenant
- Dedicated audit log storage bucket per tenant (tenant-controlled S3/equivalent)
- Dedicated key management infrastructure per tenant
- Governance control plane shared; all data planes isolated

When to use:
- Customers subject to SEC Regulation SP (Safeguard Rule)
- Customers handling Material Non-Public Information (MNPI)
- Customers with contractual requirements for physical data separation
- Customers subject to jurisdiction-specific data localization requirements

### Tier 3: Dedicated Isolation (For large institutional customers)

Architecture:
- Dedicated governance infrastructure in tenant-controlled network segment
- Platform manages deployment and lifecycle via control plane
- Tenant holds all encryption keys in their own HSM
- Platform cannot access tenant data without tenant authorization
- Separate Kubernetes namespace, separate compute, separate networking

When to use:
- Large institutional investors with their own regulatory obligations
- Customers who must demonstrate to their own regulators that data stays in their control
- Customers with conflicting regulatory requirements that cannot be satisfied in shared infra

---

## Cross-Tenant Data Handling

Certain platform-level operations require reasoning across tenants:

**Permitted cross-tenant operations:**
- Anonymous aggregate statistics (cost benchmarking, quality trends) — no individual tenant data exposed
- Platform-level compliance monitoring — sees compliance status per tenant, not content
- Model performance aggregate reporting — sees aggregate scores, not tenant-specific queries
- Security threat detection — pattern matching across events, never content inspection

**Prohibited cross-tenant operations:**
- Any query that returns tenant-specific governance content to a different tenant
- Policy set from Tenant A applied to Tenant B
- Audit trail from Tenant A accessible by Tenant B
- Risk scores from Tenant A visible to Tenant B

All cross-tenant operations by platform administrators are logged in a separate
privileged access audit trail that is subject to regular review.

---

## Data Residency

For tenants with data residency requirements, governance data is stored in the tenant's
designated regions:

```yaml
# Tenant configuration example
data_residency:
  primary_region: eu-west-1         # where governance data is stored
  allowed_processing_regions: [eu-west-1, eu-central-1]
  prohibited_regions: [us-east-1, ap-southeast-1]
  data_localization_required: true
```

The Governance Platform enforces residency at the storage layer. Cross-region replication
is disabled for tenants with data localization requirements. The Platform Operations team
cannot bypass residency configuration without triggering an audit alert.
