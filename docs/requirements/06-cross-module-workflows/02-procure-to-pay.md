# Procure-to-Pay Pathway

| Field | Value |
|---|---|
| Module | XWF |
| Sub-module | P2P |
| Status | Draft — pending verification |
| Source | §5.2 B; §7.2 |

## 1. Scope
End-to-end PR/PO/GRN/invoice/payment with three-way match.

## 2. Exclusions
Non-PO invoices only under explicit exception policy.

## 3. Actors and Permissions
- Requestor
- Buyer
- Receiver
- AP
- Controller

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| XWF-P2P-FR-001 | Approved PR converts to PO (via RFQ/contract/direct policy). |
| XWF-P2P-FR-002 | Issued PO enables GRN in Inventory. |
| XWF-P2P-FR-003 | Vendor invoice in FIN AP matches PO+GRN. |
| XWF-P2P-FR-004 | Approved payment disburses and posts GL. |
| XWF-P2P-FR-005 | Vendor performance updates on receipt/payment outcomes. |

## 5. Workflow and State Transitions
PR -> PO -> GRN -> InvoiceMatched -> PaymentDisbursed.

## 6. Data / Entities and Validation
- Shared identifiers: prId, poId, grnId, invoiceId, paymentId

## 7. Business Rules
| ID | Rule |
|---|---|
| XWF-P2P-BR-001 | Payment cannot precede successful match/approved exception. |
| XWF-P2P-BR-002 | All hops idempotent. |

## 8. Approvals
Value-based approvals on PR/PO/payment.

## 9. APIs and Module Ownership
**Owner:** XWF

### APIs
- `Existing module APIs`

### Events Published
- `PurchaseOrderIssued`
- `GoodsReceived`
- `VendorInvoiceMatched`
- `ApPaymentDisbursed`

### Events Consumed
- `PurchaseRequisitionApproved`
- `ApprovalDecisionMade`

## 10. Notifications
- Match variance
- Payment due

## 11. Reports
- P2P cycle time
- Match exception rate

## 12. Audit, Retention, and Privacy
Commercial + financial audit trail complete.

## 13. Failure, Idempotency, and Concurrency
- Partial GRN supports partial invoice match
- Dead-letter alerts on posting failures

## 14. Non-Functional Requirements
- Financial posting exactly-once effective

## 15. Dependencies
- PRC
- INV
- FIN

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| XWF-P2P-AC-001 | Three-way match success path pays vendor once. |
| XWF-P2P-AC-002 | Missing GRN blocks match. |

## 17. Open Assumptions
- Evaluated receipt settlement optional later.

## 18. Source Traceability
Mapped from `§5.2 B; §7.2` in `Healthcare-ERP-Pathway-and-Workflow.md`.
