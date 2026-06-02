/**
 * Policy evaluator with local decision cache.
 * Checks L1 cache first, then calls Policy Service on miss.
 */

import { GovernanceClient } from '../client';
import { GovernanceContext, PolicyDecision, PolicyEnforcement } from '../models/governance';
import { GovernancePolicyViolation } from '../exceptions';

export class PolicyEvaluator {
  private readonly cache = new Map<string, { decision: PolicyDecision; cachedAt: number }>();
  private readonly ttlMs: number;

  constructor(private readonly client: GovernanceClient) {
    this.ttlMs = (client.config.cacheTtlSeconds ?? 300) * 1000;
  }

  async evaluate(context: GovernanceContext): Promise<PolicyDecision> {
    const cacheKey = this.computeCacheKey(context);
    const cached = this.cache.get(cacheKey);

    if (cached && Date.now() - cached.cachedAt < this.ttlMs) {
      return cached.decision;
    }

    const rawDecision = await this.client.http.post<PolicyDecision>(
      '/v1/policies/evaluate',
      {
        artifact_id: context.artifactId,
        tenant_id: context.tenantId,
        context: {
          model: context.model,
          has_tools: context.hasTools,
          has_system_prompt: context.hasSystemPrompt,
        },
      },
    );

    const decision: PolicyDecision = {
      ...rawDecision,
      enforce() {
        if (this.enforcement === PolicyEnforcement.BLOCK) {
          throw new GovernancePolicyViolation(
            this.artifactId,
            this.violations,
            this.decisionId,
          );
        }
      },
    };

    this.cache.set(cacheKey, { decision, cachedAt: Date.now() });
    return decision;
  }

  invalidate(artifactId: string): void {
    for (const key of this.cache.keys()) {
      if (key.includes(artifactId)) {
        this.cache.delete(key);
      }
    }
  }

  private computeCacheKey(context: GovernanceContext): string {
    return `${context.artifactId}:${context.tenantId}:${context.model}`;
  }
}
