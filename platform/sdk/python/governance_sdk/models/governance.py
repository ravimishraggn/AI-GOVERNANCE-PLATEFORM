"""
Core governance data models for the Python SDK.
These models mirror the platform's canonical data model for governance entities.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AuditEventType(str, Enum):
    AGENT_INVOKED = "agent.invoked"
    MODEL_CALLED = "model.called"
    TOOL_CALLED = "tool.called"
    WORKFLOW_STARTED = "workflow.started"
    WORKFLOW_COMPLETED = "workflow.completed"
    WORKFLOW_STEP_COMPLETED = "workflow.step.completed"
    HUMAN_ESCALATION_TRIGGERED = "workflow.human_escalation.triggered"
    POLICY_EVALUATED = "policy.evaluated"
    POLICY_VIOLATION = "policy.violation"
    SECURITY_EVENT = "security.event"
    RAG_RETRIEVAL = "rag.retrieval"


class PolicyEnforcement(str, Enum):
    ALLOW = "allow"
    WARN = "warn"
    BLOCK = "block"


@dataclass
class GovernanceContext:
    """Governance context for an AI invocation."""
    artifact_id: str
    tenant_id: str
    invocation_id: str
    model: str
    message_count: int = 0
    has_system_prompt: bool = False
    has_tools: bool = False
    session_id: str | None = None
    user_id: str | None = None
    additional_context: dict[str, Any] = field(default_factory=dict)


@dataclass
class PolicyDecision:
    """Result of a policy evaluation."""
    decision_id: str
    artifact_id: str
    enforcement: PolicyEnforcement
    applied_policies: list[str] = field(default_factory=list)
    violations: list[PolicyViolation] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    exceptions_applied: list[str] = field(default_factory=list)

    def enforce(self) -> None:
        """Raise GovernancePolicyViolation if enforcement is BLOCK."""
        from governance_sdk.exceptions import GovernancePolicyViolation
        if self.enforcement == PolicyEnforcement.BLOCK:
            raise GovernancePolicyViolation(
                artifact_id=self.artifact_id,
                violations=self.violations,
                decision_id=self.decision_id,
            )


@dataclass
class PolicyViolation:
    policy_id: str
    policy_name: str
    violation_description: str
    remediation_hint: str | None = None


@dataclass
class InvocationRecord:
    """Record of a governed AI invocation for audit purposes."""
    invocation_id: str
    model: str
    latency_ms: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    tool_calls: list[dict] = field(default_factory=list)
    retrieval_context: dict | None = None


@dataclass
class RiskProfile:
    artifact_id: str
    composite_score: float
    risk_tier: str
    dimension_scores: dict[str, float] = field(default_factory=dict)


@dataclass
class EvaluationResult:
    artifact_id: str
    benchmark_id: str
    pass_fail: str
    scores: dict[str, float] = field(default_factory=dict)
    regression_detected: bool = False
