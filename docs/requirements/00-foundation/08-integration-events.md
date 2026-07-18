# Integration Events (Outbox/Inbox)

| Field | Value |
|---|---|
| Module | FND |
| Sub-module | EVT |
| Status | Draft — pending verification |
| Source | §2 Integration hub; all module integration triggers |

## 1. Scope
Reliable asynchronous integration between modules using transactional outbox and inbox deduplication, schema-versioned event contracts.

## 2. Exclusions
External enterprise service bus products; public webhook marketplace in Phase 1.

## 3. Actors and Permissions
- Platform engineers — monitor bus health
- All modules — publish/consume via shared abstractions

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| FND-EVT-FR-001 | State-changing use cases that require cross-module effects shall publish integration events in the same DB transaction as the write (outbox pattern). |
| FND-EVT-FR-002 | Consumers shall process events idempotently via inbox dedupe keys. |
| FND-EVT-FR-003 | Event contracts shall be versioned (v1, v2) and backward compatible within major version. |
| FND-EVT-FR-004 | Failed handlers shall retry with backoff and then dead-letter with alerting. |
| FND-EVT-FR-005 | Ordering shall be guaranteed per aggregate partition key where required (e.g., stock item). |
| FND-EVT-FR-006 | There shall be an admin replay capability for selected event types. |

## 5. Workflow and State Transitions
Outbox: `Pending -> Dispatched -> Completed | Failed`.
Inbox: `Received -> Processed | DeadLetter`.

## 6. Data / Entities and Validation
- `OutboxMessage`, `InboxMessage`, `DeadLetterMessage`, `EventSchemaRegistry` entry
- Envelope: eventId, eventType, occurredAt, correlationId, causationId, partitionKey, payload, version

## 7. Business Rules
| ID | Rule |
|---|---|
| FND-EVT-BR-001 | No module may call another module's internal repositories. |
| FND-EVT-BR-002 | Sync query APIs are allowed for reads; writes across modules go through events or explicit application services at the host composition root only when strongly consistent and documented. |

## 8. Approvals
Replay of financial/clinical events may require Compliance/Finance approval in production.

## 9. APIs and Module Ownership
**Owner:** FND

### APIs
- `GET /api/fnd/events/outbox/health`
- `GET /api/fnd/events/dead-letters`
- `POST /api/fnd/events/dead-letters/{id}/replay`

### Events Published
- `EventDeadLetterCreated`

### Events Consumed
- None

## 10. Notifications
- Alert ops on dead-letter threshold

## 11. Reports
- Event throughput
- Dead-letter aging
- Consumer lag

## 12. Audit, Retention, and Privacy
Event payloads avoid unnecessary PHI; use references. Event archives follow retention policy.

## 13. Failure, Idempotency, and Concurrency
- Publisher uses transaction + outbox.
- Consumer idempotent by eventId.
- Poison message isolation after N attempts.

## 14. Non-Functional Requirements
- At-least-once delivery semantics.
- Dispatch lag P95 < 5s normal load.

## 15. Dependencies
- PostgreSQL
- All modules

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| FND-EVT-AC-001 | Stock issue publishes event and inventory write atomically. |
| FND-EVT-AC-002 | Duplicate delivery does not double-post financial entries. |
| FND-EVT-AC-003 | Architecture tests enforce module boundary rules. |

## 17. Open Assumptions
- In-process dispatcher is acceptable for modular monolith MVP; can swap to broker later.

## 18. Source Traceability
Mapped from `§2 Integration hub; all module integration triggers` in `Healthcare-ERP-Pathway-and-Workflow.md`.
