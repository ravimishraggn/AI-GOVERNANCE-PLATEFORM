-- Governance Metadata Store Schema
-- Central metadata for all registered AI artifacts

-- Tenants
CREATE TABLE tenants (
    tenant_id           UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    canonical_name      VARCHAR(200)    UNIQUE NOT NULL,
    display_name        VARCHAR(200)    NOT NULL,
    tenant_type         VARCHAR(50)     NOT NULL,
    isolation_tier      VARCHAR(50)     NOT NULL DEFAULT 'Logical',
    status              VARCHAR(50)     NOT NULL DEFAULT 'Onboarding',
    config              JSONB           NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

-- Artifact registry (all artifact types)
CREATE TABLE artifacts (
    artifact_id         UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID            NOT NULL REFERENCES tenants(tenant_id),
    canonical_name      VARCHAR(300)    NOT NULL,
    artifact_type       VARCHAR(50)     NOT NULL,  -- Agent, Model, Prompt, Dataset, Tool, Workflow
    version             VARCHAR(50)     NOT NULL,
    display_name        VARCHAR(200),
    description         TEXT,
    status              VARCHAR(50)     NOT NULL DEFAULT 'Development',
    metadata            JSONB           NOT NULL DEFAULT '{}',
    owning_team         VARCHAR(200),
    business_owner      JSONB,
    technical_owner     JSONB,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    created_by          VARCHAR(200),
    UNIQUE (tenant_id, canonical_name, version)
);

CREATE INDEX idx_artifacts_tenant_type ON artifacts (tenant_id, artifact_type, status);
CREATE INDEX idx_artifacts_canonical ON artifacts (canonical_name, version);

-- Risk profiles
CREATE TABLE risk_profiles (
    profile_id          UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    artifact_id         UUID            NOT NULL REFERENCES artifacts(artifact_id),
    tenant_id           UUID            NOT NULL,
    composite_score     NUMERIC(4,2)    NOT NULL,
    risk_tier           VARCHAR(50)     NOT NULL,
    dimension_scores    JSONB           NOT NULL DEFAULT '{}',
    risk_factors        JSONB           NOT NULL DEFAULT '[]',
    risk_acceptance     JSONB,          -- NULL if no active acceptance
    methodology         VARCHAR(200)    NOT NULL,
    confidence          NUMERIC(4,3)    NOT NULL,
    assessed_at         TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    next_review         TIMESTAMPTZ
);

CREATE INDEX idx_risk_profiles_artifact ON risk_profiles (artifact_id, assessed_at DESC);
CREATE INDEX idx_risk_profiles_tier ON risk_profiles (tenant_id, risk_tier);

-- Policies
CREATE TABLE policies (
    policy_id           UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID,           -- NULL = platform-scoped
    canonical_name      VARCHAR(200)    NOT NULL,
    domain              VARCHAR(100)    NOT NULL,
    scope               VARCHAR(50)     NOT NULL,
    version             VARCHAR(50)     NOT NULL,
    status              VARCHAR(50)     NOT NULL DEFAULT 'Draft',
    rule_set            JSONB           NOT NULL,
    applicability       JSONB           NOT NULL,
    enforcement_mode    VARCHAR(50)     NOT NULL DEFAULT 'Block',
    parent_policy_id    UUID            REFERENCES policies(policy_id),
    effective_from      TIMESTAMPTZ     NOT NULL,
    effective_to        TIMESTAMPTZ,
    approval_record     JSONB,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    UNIQUE (canonical_name, version, COALESCE(tenant_id, '00000000-0000-0000-0000-000000000000'))
);

-- Approval requests
CREATE TABLE approval_requests (
    request_id          UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID            NOT NULL,
    artifact_id         UUID            NOT NULL REFERENCES artifacts(artifact_id),
    request_type        VARCHAR(100)    NOT NULL,
    requester_id        VARCHAR(200)    NOT NULL,
    submitted_at        TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    current_stage       VARCHAR(100),
    sla_deadline        TIMESTAMPTZ,
    final_outcome       VARCHAR(50),
    conditions          JSONB,
    workflow_template   VARCHAR(200)    NOT NULL,
    review_package      JSONB
);

CREATE INDEX idx_approval_requests_artifact ON approval_requests (artifact_id, submitted_at DESC);
CREATE INDEX idx_approval_requests_status ON approval_requests (tenant_id, final_outcome, sla_deadline);

-- Row-Level Security on all tenant-scoped tables
ALTER TABLE artifacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE risk_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE approval_requests ENABLE ROW LEVEL SECURITY;

CREATE POLICY artifacts_tenant_rls ON artifacts
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);
CREATE POLICY risk_profiles_tenant_rls ON risk_profiles
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);
CREATE POLICY approval_requests_tenant_rls ON approval_requests
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);
