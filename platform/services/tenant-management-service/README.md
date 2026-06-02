# Tenant Management Service

## Purpose

Handles tenant provisioning, configuration, quota management, and lifecycle management
for all tenants on the Governance Platform.

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/tenants` | Provision new tenant |
| GET | `/v1/tenants/{tenant_id}` | Get tenant record |
| PUT | `/v1/tenants/{tenant_id}` | Update tenant configuration |
| DELETE | `/v1/tenants/{tenant_id}` | Offboard tenant (admin only) |
| POST | `/v1/tenants/{tenant_id}/policy-sets` | Configure tenant policy set |
| GET | `/v1/tenants/{tenant_id}/quotas` | Get quota usage |
| PUT | `/v1/tenants/{tenant_id}/quotas` | Update quota configuration |
| GET | `/v1/tenants/{tenant_id}/governance-health` | Get governance health score |
| POST | `/v1/tenants/{tenant_id}/suspend` | Suspend tenant (admin only) |

## Tenant Provisioning Process

1. Receive tenant configuration (name, type, regulatory profile, isolation tier)
2. Create tenant record in governance metadata store
3. Initialize tenant-specific encryption keys in KMS
4. Apply appropriate isolation tier provisioning
5. Load default policy set for tenant's regulatory profile
6. Configure risk tolerance defaults based on tenant type
7. Set up notification channels and governance contacts
8. Generate onboarding checklist and send welcome notification
9. Record provisioning audit event

## Tenant Governance Health Score

A composite score (0–100) reflecting the tenant's governance hygiene:
- Registration coverage (% of artifacts registered)
- Compliance posture (% of controls satisfied)
- Evaluation coverage (% of artifacts with current evaluations)
- Risk acceptance quality (% with documented, non-expired acceptances)
- Open governance items (outstanding reviews, expired certifications)

Health score < 70 triggers a governance review request to the tenant's governance contact.
