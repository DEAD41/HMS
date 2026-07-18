# Purchase Order Issuance

| Field | Value |
|---|---|
| Module | PRC |
| Sub-module | PO |
| Status | Draft — pending verification |
| Source | §7.1 PO; §7.2 step 5; feeds FIN/INV |

## 1. Scope
Issue purchase orders to vendors from approved PR/award/contract with terms.

## 2. Exclusions
Supplier ASN advanced ship notices deep EDI beyond basic.

## 3. Actors and Permissions
- Buyer
- Procurement Manager
- Vendor (receive PO)

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| PRC-PO-FR-001 | Create PO headers/lines with prices, taxes, delivery store, and terms. |
| PRC-PO-FR-002 | Submit for approval based on value. |
| PRC-PO-FR-003 | Issue/send PO to vendor and freeze commercial terms. |
| PRC-PO-FR-004 | Support amendments and cancellations. |
| PRC-PO-FR-005 | Expose PO to Inventory receiving and Financials match. |

## 5. Workflow and State Transitions
PO: `Draft -> InApproval -> Approved -> Issued -> PartiallyReceived -> Received | Cancelled | Closed`.

## 6. Data / Entities and Validation
- `PurchaseOrder`
- `PurchaseOrderLine`
- `PoAmendment`

## 7. Business Rules
| ID | Rule |
|---|---|
| PRC-PO-BR-001 | Issued PO required for standard GRN. |
| PRC-PO-BR-002 | Cannot receive more than open qty beyond tolerance. |
| PRC-PO-BR-003 | Vendor must be active. |

## 8. Approvals
PO approval via procurement approval policies.

## 9. APIs and Module Ownership
**Owner:** PRC

### APIs
- `POST /api/prc/purchase-orders`
- `POST /api/prc/purchase-orders/{id}/issue`
- `POST /api/prc/purchase-orders/{id}/amend`

### Events Published
- `PurchaseOrderIssued`
- `PurchaseOrderAmended`
- `PurchaseOrderCancelled`

### Events Consumed
- `PurchaseRequisitionApproved`
- `AwardDecisionMade`
- `ContractActivated`
- `ApprovalDecisionMade`

## 10. Notifications
- PO issued to stakeholders

## 11. Reports
- PO register
- Open commitments

## 12. Audit, Retention, and Privacy
PO commercial record retained; amendments audited.

## 13. Failure, Idempotency, and Concurrency
- Issue idempotent
- Commitment updates concurrency safe

## 14. Non-Functional Requirements
- Issue PO < 300ms

## 15. Dependencies
- PR/Award/Contract
- INV GRN
- FIN AP/Budget

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| PRC-PO-AC-001 | Issued PO appears for receiving against lines. |
| PRC-PO-AC-002 | Commitment visible to budget control. |

## 17. Open Assumptions
- PDF/email send via notifications.

## 18. Source Traceability
Mapped from `§7.1 PO; §7.2 step 5; feeds FIN/INV` in `Healthcare-ERP-Pathway-and-Workflow.md`.
