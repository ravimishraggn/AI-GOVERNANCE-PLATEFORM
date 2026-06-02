# Governance Gateway

## Purpose

The Governance Gateway is the single API entry point for the entire Governance Platform.
It handles routing, authentication, authorization, rate limiting, and request validation
for all incoming governance API requests.

## Responsibilities

- Authenticate all incoming requests against the enterprise identity provider
- Authorize requests based on caller identity, tenant context, and requested operation
- Route requests to the appropriate downstream governance service
- Enforce rate limits per tenant and per calling service
- Validate API contracts before forwarding
- Log all requests and responses for audit purposes
- Return standardized error responses

## API Surface

- REST API: `/api/v1/...` — synchronous operations
- GraphQL: `/graphql` — complex query operations (Phase 2+)
- WebSocket: `/events/...` — event subscriptions
- Health: `/health`, `/ready` — operational endpoints

## Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Availability | 99.999% |
| Request latency P50 | < 5ms (routing overhead) |
| Request latency P99 | < 20ms (routing overhead) |
| Max throughput | 50,000 req/sec |

## Configuration

See [config/config.yaml](config/config.yaml) for all configuration options.

## Dependencies

- Identity Provider (authentication)
- Policy Service (policy evaluation for authorization)
- Audit Service (request logging)
- All downstream governance services (routing targets)
