# Canonical Events, Errors & Reconciliation

| Field | Value |
|---|---|
| Module | XWF |
| Sub-module | EVT |
| Status | Draft — pending verification |
| Source | §2 hub; all integration trigger sections; governance audit |

## 1. Scope
Define canonical event catalog expectations, error handling, dead-letter, and reconciliation jobs between modules.

## 2. Exclusions
External enterprise integrator mapping tools.

## 3. Actors and Permissions
- Platform Engineer
- Module Owners
- Controllers/Compliance for financial/clinical recon

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| XWF-EVT-FR-001 | Maintain versioned event catalog with producer, payload key fields, consumers, and idempotency keys. |
| XWF-EVT-FR-002 | All critical financial/stock/clinical cross effects covered by reconciliation reports. |
| XWF-EVT-FR-003 | Dead-letter messages alert and are replayable after fix. |
| XWF-EVT-FR-004 | Daily recon: stock vs financial COGS; charges vs AR; payroll vs GL; PO commitments vs GRN/AP. |
| XWF-EVT-FR-005 | Document compensating transactions for each critical failure mode. |

## 5. Workflow and State Transitions
Event processing: Received -> Processed | DeadLetter -> Replayed -> Processed.
Recon: `Scheduled -> Running -> Clean | BreaksFound -> Resolved`.

## 6. Data / Entities and Validation
- `EventCatalogEntry`
- `ReconciliationRun`
- `ReconciliationBreak`

## 7. Business Rules
| ID | Rule |
|---|---|
| XWF-EVT-BR-001 | Breaks do not auto-mute; ownership required for resolution. |
| XWF-EVT-BR-002 | Replay must remain idempotent. |

## 8. Approvals
Replay of financial/clinical events in production may require Compliance/Finance approval.

## 9. APIs and Module Ownership
**Owner:** XWF

### APIs
- `GET /api/fnd/events/catalog`
- `POST /api/fnd/recon/runs`
- `GET /api/fnd/recon/breaks`

### Events Published
- `ReconciliationBreakFound`
- `EventDeadLetterCreated`

### Events Consumed
- `All integration events`

## 10. Notifications
- Dead-letter threshold
- Unresolved recon breaks

## 11. Reports
- Recon dashboards listed above

## 12. Audit, Retention, and Privacy
Recon evidence retained with financial close packages.

## 13. Failure, Idempotency, and Concurrency
- Handlers idempotent
- Recon jobs restartable
- Poison message isolation

## 14. Non-Functional Requirements
- Critical event hop P95 < 5s
- Daily recon completes in batch window

## 15. Dependencies
- FND EVT
- All modules

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| XWF-EVT-AC-001 | Duplicate event delivery does not duplicate money/stock movements. |
| XWF-EVT-AC-002 | Dead-letter replay after fix converges system. |
| XWF-EVT-AC-003 | Daily recon detects intentional mismatch test. |

## 17. Open Assumptions
- In-process dispatcher acceptable for modular monolith MVP.

## 18. Source Traceability
Mapped from `§2 hub; all integration trigger sections; governance audit` in `Healthcare-ERP-Pathway-and-Workflow.md`.
