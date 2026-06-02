# Tenant Onboarding Checklist

Complete this checklist when onboarding a new tenant to the AI Governance Platform.
Each step must be verified before the tenant proceeds to the next.

---

## Phase 1: Tenant Provisioning

- [ ] **1.1** Collect tenant profile information (see `templates/enterprise-tenant-template.yaml`)
- [ ] **1.2** Determine isolation tier (Logical / Namespace / Dedicated)
- [ ] **1.3** Identify applicable regulatory frameworks from tenant profile
- [ ] **1.4** Provision tenant via Tenant Management Service API
- [ ] **1.5** Verify encryption keys generated and accessible to tenant
- [ ] **1.6** Confirm data residency region matches tenant requirements
- [ ] **1.7** Set initial quota configuration based on subscription tier

## Phase 2: Governance Configuration

- [ ] **2.1** Load applicable regulatory policy set (based on jurisdiction + regulatory profile)
- [ ] **2.2** Configure risk tolerance defaults (or accept platform defaults)
- [ ] **2.3** Configure approval workflow templates for tenant's governance structure
- [ ] **2.4** Set up governance contacts (primary, compliance, security, technical)
- [ ] **2.5** Configure notification channels (email, Slack, webhook) for governance events
- [ ] **2.6** Verify tenant can access Developer Portal with correct tenant context

## Phase 3: Compliance Setup

- [ ] **3.1** Confirm applicable compliance frameworks are active for tenant
- [ ] **3.2** Review and acknowledge platform's compliance coverage for tenant's jurisdiction
- [ ] **3.3** Identify any compliance gaps at onboarding (document remediation plan)
- [ ] **3.4** Schedule first compliance posture review (within 30 days of go-live)
- [ ] **3.5** Provide access to compliance evidence package generation for compliance officer

## Phase 4: Team Enablement

- [ ] **4.1** Share Developer Quickstart Guide with all product teams
- [ ] **4.2** Conduct governance onboarding session (90 minutes, mandatory for tech leads)
- [ ] **4.3** Provide governance manifest templates and examples
- [ ] **4.4** Verify at least one successful artifact registration in staging environment
- [ ] **4.5** Verify Governance SDK integrated in at least one test application

## Phase 5: Go-Live Verification

- [ ] **5.1** Confirm governance gateway is accessible from tenant's environment
- [ ] **5.2** Confirm audit events are flowing correctly (test via audit trail query)
- [ ] **5.3** Confirm telemetry is flowing and visible in cost dashboard
- [ ] **5.4** Confirm policy evaluation latency is within SLA (< 10ms P99)
- [ ] **5.5** Schedule 30-day governance health review

## Post-Onboarding

- [ ] **6.1** Assign a Governance Relationship Manager for the first 90 days
- [ ] **6.2** Schedule monthly governance review cadence for first quarter
- [ ] **6.3** Add tenant to platform governance communications list
- [ ] **6.4** Document any special governance configurations in tenant record
