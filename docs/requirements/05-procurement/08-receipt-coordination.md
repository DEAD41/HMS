# Goods Receipt Coordination with Store

| Field | Value |
|---|---|
| Module | PRC |
| Sub-module | GRC |
| Status | Draft — pending verification |
| Source | §7.1 GRN coordination; §7.2 step 6 |

## 1. Scope
Coordinate expected receipts, tolerances, and close-out between Procurement PO and Inventory GRN.

## 2. Exclusions
Does not replace Inventory GRN execution.

## 3. Actors and Permissions
- Buyer
- Receiving Clerk
- Procurement Manager

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| PRC-GRC-FR-001 | Provide receiving expectations/worklist from issued POs. |
| PRC-GRC-FR-002 | Configure over/under delivery tolerances. |
| PRC-GRC-FR-003 | Consume GoodsReceived events to update PO line statuses. |
| PRC-GRC-FR-004 | Close PO lines when complete. |
| PRC-GRC-FR-005 | Handle short-close with reason. |

## 5. Workflow and State Transitions
PO line receiving state updated: `Open -> Partial -> Complete | ShortClosed`.

## 6. Data / Entities and Validation
- PO receiving projection
- Tolerance policy

## 7. Business Rules
| ID | Rule |
|---|---|
| PRC-GRC-BR-001 | Short-close requires reason and permission/approval when value remains. |

## 8. Approvals
Short-close above threshold approval required.

## 9. APIs and Module Ownership
**Owner:** PRC

### APIs
- `GET /api/prc/receiving-worklist`
- `POST /api/prc/purchase-orders/{id}/short-close`

### Events Published
- `PurchaseOrderReceivingUpdated`
- `PurchaseOrderClosed`

### Events Consumed
- `GoodsReceived`
- `GoodsRejected`

## 10. Notifications
- Overdue expected delivery alerts

## 11. Reports
- On-time delivery inputs
- Open PO receiving aging

## 12. Audit, Retention, and Privacy
Coordination actions audited.

## 13. Failure, Idempotency, and Concurrency
- Event handler idempotent by GRN id

## 14. Non-Functional Requirements
- PO status update < 5s after GRN

## 15. Dependencies
- INV GRN
- PO
- Vendor performance

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| PRC-GRC-AC-001 | GRN against PO updates PO remaining qty. |
| PRC-GRC-AC-002 | Fully received PO can close. |

## 17. Open Assumptions
- ASN optional later.

## 18. Source Traceability
Mapped from `§7.1 GRN coordination; §7.2 step 6` in `Healthcare-ERP-Pathway-and-Workflow.md`.
