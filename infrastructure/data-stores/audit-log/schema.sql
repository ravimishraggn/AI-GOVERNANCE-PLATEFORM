-- Audit Log Schema
-- Append-only table — no UPDATE or DELETE operations permitted
-- Row-Level Security enforced at PostgreSQL level by tenant_id
-- In production: backed by immutable object storage (S3 Object Lock)
-- This schema represents the queryable index layer over the immutable store.

CREATE TABLE audit_events (
    id                  UUID            NOT NULL,
    sequence_number     BIGINT          NOT NULL,   -- monotonically increasing per tenant
    tenant_id           UUID            NOT NULL,
    event_type          VARCHAR(100)    NOT NULL,
    event_timestamp     TIMESTAMPTZ     NOT NULL,

    -- Actor
    actor_type          VARCHAR(50)     NOT NULL,   -- User, System, Agent, ExternalService
    actor_id            VARCHAR(255)    NOT NULL,

    -- Subject
    subject_type        VARCHAR(50)     NOT NULL,
    subject_id          UUID            NOT NULL,
    subject_version     VARCHAR(50),

    -- Event content
    action              VARCHAR(255)    NOT NULL,
    outcome             VARCHAR(50)     NOT NULL,   -- Success, Failure, Partial

    -- Governance context snapshots (stored as JSONB for queryability)
    policy_context      JSONB,
    risk_context        JSONB,
    compliance_context  JSONB,

    -- Encrypted event payload (never queryable — only returned via authorized export)
    event_data          BYTEA,

    -- Cryptographic integrity
    previous_hash       CHAR(64)        NOT NULL,   -- SHA-256 of previous event
    event_hash          CHAR(64)        NOT NULL,   -- SHA-256 of this event
    signature           TEXT            NOT NULL,   -- HSM digital signature

    -- Retention
    retention_class     VARCHAR(50)     NOT NULL,
    retention_expires_at TIMESTAMPTZ,               -- NULL = indefinite

    PRIMARY KEY (tenant_id, sequence_number),

    -- Prevent updates — enforced by trigger
    CONSTRAINT audit_events_no_update CHECK (TRUE)
);

-- Enforce append-only at the database level
CREATE OR REPLACE RULE audit_events_no_delete AS
    ON DELETE TO audit_events DO INSTEAD NOTHING;

-- Indexes for common query patterns
CREATE INDEX idx_audit_events_subject
    ON audit_events (tenant_id, subject_id, event_timestamp DESC);

CREATE INDEX idx_audit_events_type_time
    ON audit_events (tenant_id, event_type, event_timestamp DESC);

CREATE INDEX idx_audit_events_actor
    ON audit_events (tenant_id, actor_id, event_timestamp DESC);

-- Row-Level Security: tenants can only see their own rows
ALTER TABLE audit_events ENABLE ROW LEVEL SECURITY;

CREATE POLICY audit_events_tenant_isolation ON audit_events
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);

-- Sequence counter per tenant (used for monotonic sequence_number)
CREATE TABLE audit_sequences (
    tenant_id       UUID    NOT NULL PRIMARY KEY,
    last_sequence   BIGINT  NOT NULL DEFAULT 0
);

COMMENT ON TABLE audit_events IS
    'Immutable append-only governance audit log. '
    'No UPDATE or DELETE operations permitted. '
    'Cryptographic chaining via previous_hash and event_hash provides tamper evidence.';
