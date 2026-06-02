"""
Policy evaluator with local decision cache.

Checks local cache first (< 1ms). On cache miss, calls Policy Service (< 10ms).
Cache is invalidated when the service receives a policy.changed event.
"""

from __future__ import annotations
import hashlib
import time
from typing import TYPE_CHECKING

from governance_sdk.models.governance import GovernanceContext, PolicyDecision

if TYPE_CHECKING:
    from governance_sdk.client import GovernanceClient


class PolicyEvaluator:
    """
    Evaluates governance policies against an invocation context.

    Uses a two-layer cache:
    - L1: In-process dict cache (thread-safe, sub-millisecond)
    - L2: Redis cache (shared across instances, ~1ms)
    - Miss: Policy Service API call (~5-10ms)
    """

    def __init__(self, client: "GovernanceClient") -> None:
        self._client = client
        self._l1_cache: dict[str, tuple[PolicyDecision, float]] = {}
        self._l1_ttl_seconds: int = client.config.cache_ttl_seconds

    async def evaluate(self, context: GovernanceContext) -> PolicyDecision:
        cache_key = self._compute_cache_key(context)

        # L1 cache check
        if cache_key in self._l1_cache:
            decision, cached_at = self._l1_cache[cache_key]
            if time.monotonic() - cached_at < self._l1_ttl_seconds:
                return decision

        # Policy Service call
        decision = await self._client.http.post(
            "/v1/policies/evaluate",
            json={
                "artifact_id": context.artifact_id,
                "tenant_id": context.tenant_id,
                "context": {
                    "model": context.model,
                    "has_tools": context.has_tools,
                    "has_system_prompt": context.has_system_prompt,
                },
            },
            timeout_ms=self._client.config.policy_evaluation_timeout_ms,
        )

        # Update L1 cache
        self._l1_cache[cache_key] = (decision, time.monotonic())

        return decision

    def invalidate(self, artifact_id: str) -> None:
        """Invalidate all cached decisions for this artifact. Called on policy.changed events."""
        keys_to_remove = [k for k in self._l1_cache if artifact_id in k]
        for k in keys_to_remove:
            del self._l1_cache[k]

    def _compute_cache_key(self, context: GovernanceContext) -> str:
        key_material = f"{context.artifact_id}:{context.tenant_id}:{context.model}"
        return hashlib.sha256(key_material.encode()).hexdigest()[:16]
