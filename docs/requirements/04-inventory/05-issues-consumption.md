# Issues & Consumption Tracking

| Field | Value |
|---|---|
| Module | INV |
| Sub-module | ISS |
| Status | Draft — pending verification |
| Source | §6.1 consumption; §6.2 step 3; §6.3 cost posting |

## 1. Scope
Issue stock to HMS pharmacy/ward/OT against patient orders or to departments/engineering, with costing.

## 2. Exclusions
Point-of-use cabinet hardware control.

## 3. Actors and Permissions
- Store Keeper
- Pharmacist
- Ward Nurse
- Biomed Engineer

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| INV-ISS-FR-001 | Create issue documents against patient/department/asset references. |
| INV-ISS-FR-002 | Decrement batches and on-hand quantities. |
| INV-ISS-FR-003 | Post COGS/cost to Financials cost centers. |
| INV-ISS-FR-004 | Expose availability to HMS. |
| INV-ISS-FR-005 | Support issue reversals via return documents. |

## 5. Workflow and State Transitions
Issue: `Draft -> Posted | Cancelled`.
Posted issues immutable; reverse via return.

## 6. Data / Entities and Validation
- `StockIssue`
- `StockIssueLine`
- `StockReturn`

## 7. Business Rules
| ID | Rule |
|---|---|
| INV-ISS-BR-001 | Cannot issue more than available (unless controlled backorder policy off). |
| INV-ISS-BR-002 | Patient issues require patient/encounter refs from HMS. |
| INV-ISS-BR-003 | Each issue emits costing event. |

## 8. Approvals
High-value issue overrides require supervisor approval.

## 9. APIs and Module Ownership
**Owner:** INV

### APIs
- `POST /api/inv/issues`
- `POST /api/inv/returns`

### Events Published
- `StockIssued`
- `StockReturned`
- `StockAvailabilityChanged`

### Events Consumed
- `MedicationDispenseRequested / OtImplantUsed / ConsumableUsed (HMS)`
- `ItemChanged`

## 10. Notifications
- Stock-out alerts

## 11. Reports
- Consumption by department
- Patient-level material cost

## 12. Audit, Retention, and Privacy
Issue documents audited; patient-linked issues PHI-minimized (ids).

## 13. Failure, Idempotency, and Concurrency
- Posted issue idempotent by requestId
- Per-batch concurrency control

## 14. Non-Functional Requirements
- Issue post P95 < 400ms

## 15. Dependencies
- HMS
- FIN
- Batches
- Reorder

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| INV-ISS-AC-001 | Patient drug issue reduces stock and posts cost+bill collaboration. |
| INV-ISS-AC-002 | Availability change visible to HMS. |

## 17. Open Assumptions
- Valuation at moving average or FIFO per item config.

## 18. Source Traceability
Mapped from `§6.1 consumption; §6.2 step 3; §6.3 cost posting` in `Healthcare-ERP-Pathway-and-Workflow.md`.
