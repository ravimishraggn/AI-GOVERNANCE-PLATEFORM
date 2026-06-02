# Notification Service

## Purpose

Event-driven notification and subscription management for governance events.
Enables product teams to receive proactive alerts without polling.

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/subscriptions` | Subscribe to governance events |
| DELETE | `/v1/subscriptions/{subscription_id}` | Unsubscribe |
| GET | `/v1/subscriptions` | List active subscriptions |
| GET | `/v1/notifications` | Get recent notifications |
| POST | `/v1/notifications/test` | Send test notification |
| PUT | `/v1/channels/{channel_id}` | Configure notification channel |

## Notification Channels

| Channel | Configuration | Use Case |
|---------|--------------|---------|
| Email | SMTP config | Human reviewers, compliance officers |
| Webhook | URL + secret | CI/CD pipeline triggers |
| Slack | Webhook URL | Team alerts |
| PagerDuty | Integration key | Critical incident escalation |
| Internal Portal | Built-in | Developer portal notification feed |

## Subscribable Event Types

See [platform/events/event-catalog.md](../../events/event-catalog.md) for the full
catalog of governance events that teams can subscribe to.

Common subscriptions:
- `policy.changed` → CI/CD pipeline webhook (triggers re-validation)
- `risk.threshold.breached` → Slack channel + email to artifact owner
- `certification.expiring` → Email to technical owner 30 days before expiry
- `evaluation.regression` → PagerDuty for critical regressions
- `approval.decision` → Email to requestor
