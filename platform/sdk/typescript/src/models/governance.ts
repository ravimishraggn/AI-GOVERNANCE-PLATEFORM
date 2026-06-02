/**
 * Core governance data models — TypeScript types.
 * Mirror the platform's canonical governance data model.
 */

export enum AuditEventType {
  AGENT_INVOKED = 'agent.invoked',
  MODEL_CALLED = 'model.called',
  TOOL_CALLED = 'tool.called',
  WORKFLOW_STARTED = 'workflow.started',
  WORKFLOW_COMPLETED = 'workflow.completed',
  RAG_RETRIEVAL = 'rag.retrieval',
  POLICY_EVALUATED = 'policy.evaluated',
  POLICY_VIOLATION = 'policy.violation',
}

export enum PolicyEnforcement {
  ALLOW = 'allow',
  WARN = 'warn',
  BLOCK = 'block',
}

export interface GovernanceContext {
  artifactId: string;
  tenantId: string;
  invocationId: string;
  model: string;
  hasTools: boolean;
  hasSystemPrompt: boolean;
  sessionId?: string;
  userId?: string;
}

export interface PolicyViolation {
  policyId: string;
  policyName: string;
  violationDescription: string;
  remediationHint?: string;
}

export interface PolicyDecision {
  decisionId: string;
  artifactId: string;
  enforcement: PolicyEnforcement;
  appliedPolicies: string[];
  violations: PolicyViolation[];
  warnings: string[];
  exceptionsApplied: string[];
  enforce(): void;  // throws GovernancePolicyViolation if BLOCK
}

export interface InvokeOptions {
  messages: Array<{ role: string; content: string }>;
  model: string;
  maxTokens?: number;
  system?: string;
  tools?: unknown[];
  [key: string]: unknown;
}

export interface InvokeResult {
  response: unknown;
  governanceContext: GovernanceContext;
  policyDecision: PolicyDecision;
  invocationId: string;
  latencyMs: number;
}

export interface RiskProfile {
  artifactId: string;
  compositeScore: number;
  riskTier: 'minimal' | 'low' | 'moderate' | 'high' | 'critical';
  dimensionScores: Record<string, number>;
}

export interface EvaluationScorecard {
  artifactId: string;
  evaluationDate: string;
  overallScore: number;
  passFailSummary: { passed: number; failed: number };
  certificationEligible: boolean;
}
