/**
 * Agent SDK — governed wrapper for AI model invocations.
 *
 * Embeds governance controls transparently into LLM calls.
 */

import { GovernanceClient } from '../client';
import { PolicyEvaluator } from '../policy/evaluator';
import { AuditEmitter } from '../audit/emitter';
import {
  GovernanceContext,
  PolicyDecision,
  AuditEventType,
  InvokeOptions,
  InvokeResult,
} from '../models/governance';

export class AgentSDK {
  private readonly policyEvaluator: PolicyEvaluator;
  private readonly auditEmitter: AuditEmitter;

  constructor(private readonly client: GovernanceClient) {
    this.policyEvaluator = new PolicyEvaluator(client);
    this.auditEmitter = new AuditEmitter(client);
  }

  async invoke(options: InvokeOptions): Promise<InvokeResult> {
    const startTime = Date.now();
    const invocationId = crypto.randomUUID();

    const context: GovernanceContext = {
      artifactId: this.client.config.artifactId,
      tenantId: this.client.config.tenantId ?? '',
      invocationId,
      model: options.model,
      hasTools: Array.isArray(options.tools) && options.tools.length > 0,
      hasSystemPrompt: options.system !== undefined,
    };

    // Pre-call: policy evaluation (synchronous, on critical path)
    const policyDecision = await this.policyEvaluator.evaluate(context);
    policyDecision.enforce(); // throws GovernancePolicyViolation if blocked

    // Execute the LLM call
    const response = await this.client.provider.invoke(options);

    const latencyMs = Date.now() - startTime;

    // Post-call: async audit + telemetry (non-blocking)
    this.auditEmitter.emit({
      eventType: AuditEventType.AGENT_INVOKED,
      context,
      policyDecision,
      invocationId,
      latencyMs,
      inputTokens: response.usage?.inputTokens ?? 0,
      outputTokens: response.usage?.outputTokens ?? 0,
    }).catch(() => {
      // Audit failures are logged but never propagate to callers
    });

    return {
      response,
      governanceContext: context,
      policyDecision,
      invocationId,
      latencyMs,
    };
  }
}

export { AgentSDK as default };
