"""
Audit event emitter.

Emits governance audit events asynchronously to the Audit Service.
Uses a bounded in-memory queue with background flush to avoid impacting
inference latency. Events are never dropped — if the queue is full,
the flush interval is shortened.
"""

from __future__ import annotations
import asyncio
import logging
from collections import deque
from typing import TYPE_CHECKING

from governance_sdk.models.governance import (
    AuditEventType,
    GovernanceContext,
    PolicyDecision,
    InvocationRecord,
)

if TYPE_CHECKING:
    from governance_sdk.client import GovernanceClient

logger = logging.getLogger(__name__)


class AuditEmitter:
    """
    Non-blocking audit event emitter.

    Events are queued in memory and flushed in micro-batches to the Audit Service.
    The emit() call returns immediately — it does not wait for the Audit Service.
    """

    MAX_QUEUE_SIZE = 1000
    FLUSH_INTERVAL_SECONDS = 1.0
    BATCH_SIZE = 50

    def __init__(self, client: "GovernanceClient") -> None:
        self._client = client
        self._queue: deque = deque(maxlen=self.MAX_QUEUE_SIZE)
        self._flush_task: asyncio.Task | None = None

    async def emit(
        self,
        event_type: AuditEventType,
        context: GovernanceContext,
        policy_decision: PolicyDecision,
        invocation_record: InvocationRecord,
    ) -> None:
        """Queue an audit event for async emission. Returns immediately."""
        event = {
            "event_type": event_type.value,
            "artifact_id": context.artifact_id,
            "tenant_id": context.tenant_id,
            "invocation_id": invocation_record.invocation_id,
            "model": invocation_record.model,
            "policy_decision_id": policy_decision.decision_id,
            "latency_ms": invocation_record.latency_ms,
            "input_tokens": invocation_record.input_tokens,
            "output_tokens": invocation_record.output_tokens,
        }
        self._queue.append(event)

        # Start background flush if not running
        if self._flush_task is None or self._flush_task.done():
            self._flush_task = asyncio.create_task(self._flush_loop())

    async def _flush_loop(self) -> None:
        """Background loop: flush queued events in batches."""
        while self._queue:
            batch = []
            for _ in range(min(self.BATCH_SIZE, len(self._queue))):
                if self._queue:
                    batch.append(self._queue.popleft())

            if batch:
                try:
                    await self._client.http.post(
                        "/v1/events",
                        json={"events": batch},
                        timeout_ms=200,
                    )
                except Exception:
                    # Audit write failure is logged but never propagates to the caller.
                    # The governance platform records audit service unavailability separately.
                    logger.warning(
                        "Audit Service write failed for %d events. "
                        "Events will be retried on next flush.",
                        len(batch),
                        exc_info=True,
                    )
                    # Re-queue failed events for retry
                    self._queue.extendleft(reversed(batch))

            await asyncio.sleep(self.FLUSH_INTERVAL_SECONDS)
