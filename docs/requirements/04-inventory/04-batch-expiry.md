# Batch & Expiry Tracking

| Field | Value |
|---|---|
| Module | INV |
| Sub-module | BCH |
| Status | Draft — pending verification |
| Source | §6.1 batch/expiry; §6.2 step 5 FEFO |

## 1. Scope
Track batches/lots, expiry dates, FEFO allocation, near-expiry flags, and expired write-offs.

## 2. Exclusions
External reverse-logistics carrier systems.

## 3. Actors and Permissions
- Pharmacist
- Store Keeper
- Finance (write-off)

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| INV-BCH-FR-001 | Maintain batch records per item/store. |
| INV-BCH-FR-002 | Allocate issues FEFO for expiry-sensitive items. |
| INV-BCH-FR-003 | Flag near-expiry batches for priority use/return. |
| INV-BCH-FR-004 | Write off expired/damaged stock with Financials posting. |
| INV-BCH-FR-005 | Support recall holds by batch. |

## 5. Workflow and State Transitions
Batch: `Available -> Hold | NearExpiry -> Expired -> WrittenOff`.
RecallHold blocks issue.

## 6. Data / Entities and Validation
- `Batch`
- `BatchHold`
- `ExpiryAlert`

## 7. Business Rules
| ID | Rule |
|---|---|
| INV-BCH-BR-001 | Expired batch cannot be issued. |
| INV-BCH-BR-002 | FEFO may be overridden only with reason + permission. |

## 8. Approvals
Write-offs require approval above threshold/policy.

## 9. APIs and Module Ownership
**Owner:** INV

### APIs
- `GET /api/inv/batches`
- `POST /api/inv/batches/{id}/hold`
- `POST /api/inv/write-offs`

### Events Published
- `BatchHoldApplied`
- `StockWrittenOff`
- `NearExpiryFlagged`

### Events Consumed
- `StockIncreased`
- `StockIssued`

## 10. Notifications
- Near-expiry alerts
- Recall hold alerts

## 11. Reports
- Expiry calendar
- Write-off register

## 12. Audit, Retention, and Privacy
Batch genealogy retained for regulatory drug traceability.

## 13. Failure, Idempotency, and Concurrency
- Write-off idempotent
- Allocation uses row locks per batch

## 14. Non-Functional Requirements
- FEFO allocation correct under concurrency

## 15. Dependencies
- Issues module
- FIN loss posting
- Notifications

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| INV-BCH-AC-001 | Near-expiry batch preferred over later expiry on dispense. |
| INV-BCH-AC-002 | Expired stock write-off posts financial loss. |

## 17. Open Assumptions
- Near-expiry threshold default 90 days configurable.

## 18. Source Traceability
Mapped from `§6.1 batch/expiry; §6.2 step 5 FEFO` in `Healthcare-ERP-Pathway-and-Workflow.md`.
