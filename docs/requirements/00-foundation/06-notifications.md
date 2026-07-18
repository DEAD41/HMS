# Notifications

| Field | Value |
|---|---|
| Module | FND |
| Sub-module | NTF |
| Status | Draft — pending verification |
| Source | §9; alerts across modules (credential expiry, reorder, approvals, variance) |

## 1. Scope
Central notification dispatch for in-app, email, and pluggable SMS/push providers.

## 2. Exclusions
Marketing campaigns; patient engagement CRM.

## 3. Actors and Permissions
- All users — receive in-app notifications
- Notification Admin — templates and channel settings
- Modules — raise notification requests

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| FND-NTF-FR-001 | Modules shall raise notifications through a shared API/event with template key and data payload. |
| FND-NTF-FR-002 | Users shall manage channel preferences within policy constraints (some compliance notices mandatory). |
| FND-NTF-FR-003 | System shall support delivery status tracking and retries for external channels. |
| FND-NTF-FR-004 | In-app notifications shall support read/unread state. |
| FND-NTF-FR-005 | Template rendering shall prevent XSS and avoid leaking unauthorized PHI fields. |

## 5. Workflow and State Transitions
Notification: `Queued -> Sending -> Sent | Failed -> DeadLetter`.
In-app message: `Unread -> Read -> Archived`.

## 6. Data / Entities and Validation
- `NotificationTemplate`, `NotificationMessage`, `DeliveryAttempt`, `UserNotificationPreference`

## 7. Business Rules
| ID | Rule |
|---|---|
| FND-NTF-BR-001 | Mandatory compliance templates ignore user opt-out for that channel if legally required. |
| FND-NTF-BR-002 | Payload fields are allow-listed per template. |

## 8. Approvals
Template publish for patient-facing content may require approval.

## 9. APIs and Module Ownership
**Owner:** FND

### APIs
- `POST /api/fnd/notifications`
- `GET /api/fnd/notifications/me`
- `POST /api/fnd/notifications/me/{id}/read`
- `PUT /api/fnd/notifications/preferences`

### Events Published
- `NotificationDispatched`
- `NotificationFailed`

### Events Consumed
- `Any module domain alert events`

## 10. Notifications
- Channel delivery itself

## 11. Reports
- Delivery failure rates
- Unread counts

## 12. Audit, Retention, and Privacy
Notification content that includes PHI follows same retention/access controls as source module; prefer deep links over embedding PHI.

## 13. Failure, Idempotency, and Concurrency
- Publish API idempotent by notificationRequestId.
- Retry with exponential backoff; poison messages to dead letter.

## 14. Non-Functional Requirements
- In-app fanout P95 < 2s.
- Email provider timeouts do not block core transactions.

## 15. Dependencies
- FND IAM
- FND Events

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| FND-NTF-AC-001 | Approval request creates in-app notification for approver. |
| FND-NTF-AC-002 | Failed email is retried and visible in dead-letter admin view. |

## 17. Open Assumptions
- SMS/push providers are optional integrations.

## 18. Source Traceability
Mapped from `§9; alerts across modules (credential expiry, reorder, approvals, variance)` in `Healthcare-ERP-Pathway-and-Workflow.md`.
