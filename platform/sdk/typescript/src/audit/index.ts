/**
 * Async audit event emitter.
 * Queues events in memory and flushes in micro-batches.
 * Never blocks the calling code.
 */

import { GovernanceClient } from '../client';
import { AuditEventType, GovernanceContext, PolicyDecision } from '../models/governance';

interface AuditEmitOptions {
  eventType: AuditEventType;
  context: GovernanceContext;
  policyDecision: PolicyDecision;
  invocationId: string;
  latencyMs: number;
  inputTokens: number;
  outputTokens: number;
}

export class AuditEmitter {
  private readonly queue: AuditEmitOptions[] = [];
  private flushTimer: ReturnType<typeof setTimeout> | null = null;

  private readonly BATCH_SIZE = 50;
  private readonly FLUSH_INTERVAL_MS = 1000;

  constructor(private readonly client: GovernanceClient) {}

  async emit(options: AuditEmitOptions): Promise<void> {
    this.queue.push(options);
    this.scheduleFlush();
  }

  private scheduleFlush(): void {
    if (this.flushTimer === null) {
      this.flushTimer = setTimeout(() => {
        this.flushTimer = null;
        void this.flush();
      }, this.FLUSH_INTERVAL_MS);
    }
  }

  private async flush(): Promise<void> {
    if (this.queue.length === 0) return;
    const batch = this.queue.splice(0, this.BATCH_SIZE);

    try {
      await this.client.http.post('/v1/events', {
        events: batch.map((e) => ({
          event_type: e.eventType,
          artifact_id: e.context.artifactId,
          tenant_id: e.context.tenantId,
          invocation_id: e.invocationId,
          model: e.context.model,
          policy_decision_id: e.policyDecision.decisionId,
          latency_ms: e.latencyMs,
          input_tokens: e.inputTokens,
          output_tokens: e.outputTokens,
        })),
      });
    } catch {
      // Audit failures are never propagated to callers.
    }

    if (this.queue.length > 0) {
      void this.flush();
    }
  }
}
