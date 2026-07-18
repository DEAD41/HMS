# Physical Verification / Cycle Counts

| Field | Value |
|---|---|
| Module | INV |
| Sub-module | CNT |
| Status | Draft — pending verification |
| Source | §6.1 physical verification; §6.2 step 6 |

## 1. Scope
Cycle counts, variance approval, and financial adjustments.

## 2. Exclusions
RFID full-store continuous inventory.

## 3. Actors and Permissions
- Store Keeper
- Inventory Controller
- Finance

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| INV-CNT-FR-001 | Create count sheets by store/bin/item. |
| INV-CNT-FR-002 | Capture counted quantities. |
| INV-CNT-FR-003 | Compute variances and route approvals. |
| INV-CNT-FR-004 | Post approved adjustments to stock and Financials. |

## 5. Workflow and State Transitions
Count: `Open -> Counting -> Review -> Approved -> Posted | Cancelled`.

## 6. Data / Entities and Validation
- `CycleCount`
- `CycleCountLine`
- `StockAdjustment`

## 7. Business Rules
| ID | Rule |
|---|---|
| INV-CNT-BR-001 | Posting adjusts batches explicitly when batch-controlled. |
| INV-CNT-BR-002 | Unapproved variances cannot post. |

## 8. Approvals
Variance above threshold uses FND approvals.

## 9. APIs and Module Ownership
**Owner:** INV

### APIs
- `POST /api/inv/counts`
- `POST /api/inv/counts/{id}/submit`
- `POST /api/inv/counts/{id}/post`

### Events Published
- `StockAdjusted`
- `CountVarianceApproved`

### Events Consumed
- `ApprovalDecisionMade`

## 10. Notifications
- Count due reminders
- High variance alerts

## 11. Reports
- Variance report
- Count accuracy

## 12. Audit, Retention, and Privacy
Count evidence retained; adjustments audited.

## 13. Failure, Idempotency, and Concurrency
- Post idempotent
- Freeze optional on counted bins

## 14. Non-Functional Requirements
- Count post transactional with financial event

## 15. Dependencies
- FIN adjustments
- FND Approvals

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| INV-CNT-AC-001 | Approved variance posts stock and financial adjustment once. |

## 17. Open Assumptions
- Blind count optional.

## 18. Source Traceability
Mapped from `§6.1 physical verification; §6.2 step 6` in `Healthcare-ERP-Pathway-and-Workflow.md`.
