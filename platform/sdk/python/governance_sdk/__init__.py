"""
AI Governance Platform SDK — Python

Embeds governance controls into AI applications with minimal code changes.
Policy evaluation, audit recording, cost attribution, and safety checks
are handled transparently by this SDK.

Usage:
    from governance_sdk import GovernanceClient
    from governance_sdk.agent import AgentSDK

    client = GovernanceClient(artifact_id="...", api_key="...")
    sdk = AgentSDK(client)
    response = await sdk.invoke(messages=messages, model="claude-sonnet-4-6")
"""

from governance_sdk.client import GovernanceClient
from governance_sdk.exceptions import (
    GovernancePolicyViolation,
    GovernanceServiceUnavailable,
    GovernanceBudgetExceeded,
    GovernanceRegistrationRequired,
)

__version__ = "1.0.0"
__all__ = [
    "GovernanceClient",
    "GovernancePolicyViolation",
    "GovernanceServiceUnavailable",
    "GovernanceBudgetExceeded",
    "GovernanceRegistrationRequired",
]
