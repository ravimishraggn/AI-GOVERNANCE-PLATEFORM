# Governance SDK — Python

The official Python SDK for integrating AI applications with the Governance Platform.
Embeds governance controls (policy evaluation, audit, cost tracking, safety checks)
into AI applications with minimal code changes.

## Installation

```bash
pip install ai-governance-sdk
# or from source:
pip install -e platform/sdk/python/
```

## Quick Start

```python
from governance_sdk import GovernanceClient
from governance_sdk.agent import AgentSDK

# Initialize the client (reads GOVERNANCE_ARTIFACT_ID and GOVERNANCE_API_KEY from env)
client = GovernanceClient(
    artifact_id="your-agent-id",
    api_key="your-governance-api-key",
    base_url="https://governance.platform.internal"
)

# Wrap your agent with governance
sdk = AgentSDK(client)

# Use exactly like the Anthropic SDK — governance is transparent
response = await sdk.invoke(
    messages=[{"role": "user", "content": "Analyze this portfolio..."}],
    model="claude-sonnet-4-6",
    max_tokens=2048
)
```

## What the SDK Does Automatically

On every `sdk.invoke()` call:

1. **Pre-call**: Checks policy decision cache (< 1ms). If miss, calls Policy Service.
2. **Pre-call**: Evaluates security context (prompt injection, data classification).
3. **Pre-call**: Enforces cost budget — blocks if this call would exceed budget.
4. **Post-call**: Emits async audit event (non-blocking).
5. **Post-call**: Records telemetry for cost attribution and quality monitoring.
6. **Post-call**: Emits lineage event if RAG context was provided.

## RAG Applications

```python
from governance_sdk.agent import RAGAgentSDK

sdk = RAGAgentSDK(client)

# Include retrieval context — lineage is recorded automatically
response = await sdk.invoke(
    messages=messages,
    model="claude-sonnet-4-6",
    retrieval_context={
        "knowledge_source_id": "ks-portfolio-docs-v2",
        "retrieved_documents": retrieved_docs,  # list of doc IDs
        "query": user_query
    }
)
```

## Agentic Workflows

```python
from governance_sdk.agent import WorkflowSDK

sdk = WorkflowSDK(client, workflow_id="wf-valuation-analysis")

# Governance checkpoints are inserted automatically at each step
async with sdk.workflow_session() as session:
    result = await session.run(inputs={"company": "Acme Corp"})
    # session.audit_trail contains the complete governance record
```

## Configuration

```python
# Full configuration
client = GovernanceClient(
    artifact_id="your-agent-id",
    api_key="your-api-key",
    base_url="https://governance.platform.internal",
    fail_open=True,           # allow calls if governance service unavailable
                              # set False for high-risk artifacts
    cache_ttl_seconds=300,    # policy decision cache TTL
    async_audit=True,         # audit writes are non-blocking (default True)
    telemetry_batch_size=50,  # telemetry events batched before sending
    budget_enforcement=True,  # enforce cost budgets
)
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|---------|
| `GOVERNANCE_ARTIFACT_ID` | Your artifact's registered ID | Yes |
| `GOVERNANCE_API_KEY` | Service account API key | Yes |
| `GOVERNANCE_BASE_URL` | Governance Platform base URL | Yes |
| `GOVERNANCE_FAIL_OPEN` | Allow calls if platform unavailable | No (default: true) |
| `GOVERNANCE_ENVIRONMENT` | deployment / staging / production | No |

## Modules

- `governance_sdk.agent` — AgentSDK, RAGAgentSDK, WorkflowSDK
- `governance_sdk.policy` — Direct policy evaluation (advanced use)
- `governance_sdk.audit` — Direct audit event emission (advanced use)
- `governance_sdk.evaluation` — Evaluation runner for CI/CD integration
- `governance_sdk.models` — All data model types
