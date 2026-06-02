# Governance SDK — TypeScript / JavaScript

Official TypeScript SDK for integrating AI applications with the Governance Platform.

## Installation

```bash
npm install @ai-platform/governance-sdk
# or
yarn add @ai-platform/governance-sdk
```

## Quick Start

```typescript
import { GovernanceClient, AgentSDK } from '@ai-platform/governance-sdk';

const client = new GovernanceClient({
  artifactId: process.env.GOVERNANCE_ARTIFACT_ID!,
  apiKey: process.env.GOVERNANCE_API_KEY!,
  baseUrl: process.env.GOVERNANCE_BASE_URL!,
});

const sdk = new AgentSDK(client);

const result = await sdk.invoke({
  messages: [{ role: 'user', content: 'Analyze this fund...' }],
  model: 'claude-sonnet-4-6',
  maxTokens: 2048,
});

console.log(result.response);
```

## What the SDK Handles

- Policy evaluation with local cache (< 1ms on cache hit)
- Security context evaluation (prompt injection detection)
- Cost budget enforcement
- Async audit event emission (non-blocking)
- Telemetry recording for cost attribution

## Configuration

```typescript
const client = new GovernanceClient({
  artifactId: 'your-agent-id',
  apiKey: 'your-api-key',
  baseUrl: 'https://governance.platform.internal',
  failOpen: true,              // allow calls if governance unavailable
  cacheTtlSeconds: 300,        // policy decision cache TTL
  asyncAudit: true,            // non-blocking audit writes (default: true)
  budgetEnforcement: true,     // enforce cost budgets
});
```

## TypeScript Types

All governance data models are fully typed. See `src/models/` for type definitions.

```typescript
import type {
  GovernanceContext,
  PolicyDecision,
  InvokeResult,
  RiskProfile,
} from '@ai-platform/governance-sdk';
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|---------|
| `GOVERNANCE_ARTIFACT_ID` | Registered artifact ID | Yes |
| `GOVERNANCE_API_KEY` | Service account API key | Yes |
| `GOVERNANCE_BASE_URL` | Platform base URL | Yes |
| `GOVERNANCE_FAIL_OPEN` | Allow on platform unavailability | No |
