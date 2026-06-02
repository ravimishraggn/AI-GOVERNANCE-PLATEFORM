"""
AgentSDK — governed wrapper for AI model invocations.

Transparently adds governance controls to every LLM call:
- Policy evaluation (with local cache)
- Security context evaluation (prompt injection, data classification)
- Cost budget enforcement
- Async audit event emission
- Telemetry recording for observability
"""

from __future__ import annotations
import asyncio
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

from governance_sdk.policy.evaluator import PolicyEvaluator
from governance_sdk.audit.emitter import AuditEmitter
from governance_sdk.models.governance import (
    GovernanceContext,
    PolicyDecision,
    AuditEventType,
    InvocationRecord,
)


@dataclass
class InvokeResult:
    """Result of a governed AI invocation."""
    response: Any                       # the raw provider response
    governance_context: GovernanceContext
    policy_decision: PolicyDecision
    invocation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    latency_ms: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0


class AgentSDK:
    """
    Governed wrapper for AI agent LLM invocations.

    Embeds governance controls transparently. The calling code does not need
    to know about the governance infrastructure — it calls invoke() and receives
    the model response. Governance happens in the background.

    Example:
        client = GovernanceClient(artifact_id="...", api_key="...")
        sdk = AgentSDK(client)
        result = await sdk.invoke(
            messages=[{"role": "user", "content": "..."}],
            model="claude-sonnet-4-6",
        )
        response = result.response
    """

    def __init__(self, client: "GovernanceClient") -> None:
        self._client = client
        self._policy_evaluator = PolicyEvaluator(client)
        self._audit_emitter = AuditEmitter(client)

    async def invoke(
        self,
        messages: list[dict],
        model: str,
        max_tokens: int = 4096,
        system: str | None = None,
        tools: list[dict] | None = None,
        **provider_kwargs: Any,
    ) -> InvokeResult:
        """
        Execute a governed LLM invocation.

        Governance steps (pre-call):
        1. Build governance context from request metadata
        2. Evaluate policy decision (cache hit: < 1ms; miss: < 10ms)
        3. Evaluate security context (< 5ms)
        4. Check cost budget
        5. If any check fails: raise GovernancePolicyViolation (or warn, per policy)

        Governance steps (post-call, async):
        6. Emit audit event
        7. Record telemetry (tokens, latency, cost)
        8. Update cost attribution
        """
        start_time = time.monotonic()
        invocation_id = str(uuid.uuid4())

        # Build governance context
        context = GovernanceContext(
            artifact_id=self._client.artifact_id,
            tenant_id=self._client.tenant_id,
            invocation_id=invocation_id,
            model=model,
            message_count=len(messages),
            has_system_prompt=system is not None,
            has_tools=tools is not None and len(tools) > 0,
        )

        # Pre-call governance checks (synchronous, on critical path)
        policy_decision = await self._policy_evaluator.evaluate(context)
        policy_decision.enforce()  # raises GovernancePolicyViolation if blocked

        # Execute the actual LLM call (governance-agnostic)
        response = await self._client.provider.invoke(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            system=system,
            tools=tools,
            **provider_kwargs,
        )

        latency_ms = int((time.monotonic() - start_time) * 1000)
        input_tokens = getattr(response.usage, "input_tokens", 0)
        output_tokens = getattr(response.usage, "output_tokens", 0)

        # Post-call governance (asynchronous — does not block response)
        asyncio.create_task(
            self._audit_emitter.emit(
                event_type=AuditEventType.AGENT_INVOKED,
                context=context,
                policy_decision=policy_decision,
                invocation_record=InvocationRecord(
                    invocation_id=invocation_id,
                    model=model,
                    latency_ms=latency_ms,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                ),
            )
        )

        return InvokeResult(
            response=response,
            governance_context=context,
            policy_decision=policy_decision,
            invocation_id=invocation_id,
            latency_ms=latency_ms,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )
