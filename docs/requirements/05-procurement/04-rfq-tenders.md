# RFQ / Tendering

| Field | Value |
|---|---|
| Module | PRC |
| Sub-module | RFQ |
| Status | Draft — pending verification |
| Source | §7.1 RFQ/tendering; §7.2 step 3 |

## 1. Scope
Send RFQs/tenders to approved vendors or use rate contracts as alternative sourcing path.

## 2. Exclusions
Public e-procurement government portal replacement.

## 3. Actors and Permissions
- Buyer
- Vendors (external response channel)
- Procurement Manager

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| PRC-RFQ-FR-001 | Create RFQ from PR lines. |
| PRC-RFQ-FR-002 | Invite approved vendors and capture due dates. |
| PRC-RFQ-FR-003 | Collect quotations (internal entry or portal). |
| PRC-RFQ-FR-004 | Close RFQ for comparison. |
| PRC-RFQ-FR-005 | Support sealed-bid mode optional. |

## 5. Workflow and State Transitions
RFQ: `Draft -> Issued -> ResponsesOpen -> Closed -> Awarded | Cancelled`.

## 6. Data / Entities and Validation
- `Rfq`
- `RfqLine`
- `RfqInvite`
- `VendorQuote`

## 7. Business Rules
| ID | Rule |
|---|---|
| PRC-RFQ-BR-001 | Only active compliant vendors invited unless exception. |
| PRC-RFQ-BR-002 | Quotes after close rejected. |

## 8. Approvals
Tender award may require committee approval.

## 9. APIs and Module Ownership
**Owner:** PRC

### APIs
- `POST /api/prc/rfqs`
- `POST /api/prc/rfqs/{id}/issue`
- `POST /api/prc/rfqs/{id}/quotes`

### Events Published
- `RfqIssued`
- `RfqClosed`

### Events Consumed
- `PurchaseRequisitionApproved`
- `VendorChanged`

## 10. Notifications
- Invite notifications
- Due date reminders

## 11. Reports
- RFQ cycle time
- Response rates

## 12. Audit, Retention, and Privacy
Commercial confidentiality for sealed bids; access controlled.

## 13. Failure, Idempotency, and Concurrency
- Issue idempotent
- Late quote rejected

## 14. Non-Functional Requirements
- Standard SLAs

## 15. Dependencies
- Vendors
- PR
- Quote comparison

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| PRC-RFQ-AC-001 | Issued RFQ visible to invited vendor response path. |
| PRC-RFQ-AC-002 | Closed RFQ ready for comparison. |

## 17. Open Assumptions
- External vendor portal Phase 4; internal capture MVP.

## 18. Source Traceability
Mapped from `§7.1 RFQ/tendering; §7.2 step 3` in `Healthcare-ERP-Pathway-and-Workflow.md`.
