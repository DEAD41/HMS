# Stock Receipt & Quality Check

| Field | Value |
|---|---|
| Module | INV |
| Sub-module | RCV |
| Status | Draft — pending verification |
| Source | §6.2 step 2; GRN with Procurement |

## 1. Scope
Receive goods against PO, quality-check, capture batch/expiry, and put away to bins.

## 2. Exclusions
Laboratory quality LIMS for materials beyond store QC checklist.

## 3. Actors and Permissions
- Receiving Clerk
- QC Inspector
- Store Keeper

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| INV-RCV-FR-001 | Create GRN against PO lines with received quantities. |
| INV-RCV-FR-002 | Capture QC pass/fail and quarantine stock. |
| INV-RCV-FR-003 | Record batch/expiry/serials. |
| INV-RCV-FR-004 | Put away accepted stock to bins and update on-hand. |
| INV-RCV-FR-005 | Notify Financials/Procurement of goods received. |

## 5. Workflow and State Transitions
GRN: `Draft -> QCPending -> PartiallyAccepted -> Accepted | Rejected`.
Stock in `Quarantine` until accepted.

## 6. Data / Entities and Validation
- `GoodsReceipt`
- `GoodsReceiptLine`
- `QCResult`
- `PutawayTask`

## 7. Business Rules
| ID | Rule |
|---|---|
| INV-RCV-BR-001 | Cannot put away more than accepted qty. |
| INV-RCV-BR-002 | Over-receipt beyond tolerance requires approval. |
| INV-RCV-BR-003 | Rejected stock not available for issue. |

## 8. Approvals
Over-receipt and QC override approvals via FND.

## 9. APIs and Module Ownership
**Owner:** INV

### APIs
- `POST /api/inv/grns`
- `POST /api/inv/grns/{id}/qc`
- `POST /api/inv/grns/{id}/putaway`

### Events Published
- `GoodsReceived`
- `GoodsRejected`
- `StockIncreased`

### Events Consumed
- `PurchaseOrderIssued`
- `VendorChanged`
- `ItemChanged`

## 10. Notifications
- QC pending aging
- Rejected delivery alerts

## 11. Reports
- GRN register
- Supplier rejection rate

## 12. Audit, Retention, and Privacy
GRN and QC evidence retained; lot genealogy available for recalls.

## 13. Failure, Idempotency, and Concurrency
- GRN confirm idempotent
- Stock increase transactional with outbox

## 14. Non-Functional Requirements
- GRN post P95 < 500ms typical

## 15. Dependencies
- PRC PO
- FIN AP match
- Batch module

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| INV-RCV-AC-001 | Accepted GRN increases on-hand and is available for three-way match. |
| INV-RCV-AC-002 | Quarantine stock not dispensable. |

## 17. Open Assumptions
- Blind receiving optional configuration.

## 18. Source Traceability
Mapped from `§6.2 step 2; GRN with Procurement` in `Healthcare-ERP-Pathway-and-Workflow.md`.
