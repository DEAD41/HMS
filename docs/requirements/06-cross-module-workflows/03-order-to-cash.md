# Order-to-Cash Pathway

| Field | Value |
|---|---|
| Module | XWF |
| Sub-module | O2C |
| Status | Draft — pending verification |
| Source | §5.2 A; HMS billing |

## 1. Scope
Charges from care delivery to invoice, claim, receipt, and AR settlement.

## 2. Exclusions
Retail non-patient POS beyond pharmacy retail.

## 3. Actors and Permissions
- Clinicians/ancillary
- Billing
- Cashier
- AR

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| XWF-O2C-FR-001 | Billable events from HMS create charges idempotently. |
| XWF-O2C-FR-002 | Invoice finalization splits self-pay vs insurance. |
| XWF-O2C-FR-003 | Claims submitted and tracked. |
| XWF-O2C-FR-004 | Receipts settle AR open items. |
| XWF-O2C-FR-005 | Aging and denials managed to closure. |

## 5. Workflow and State Transitions
Charge -> Invoice Finalized -> Claim/AR Open -> Receipt/Settlement.

## 6. Data / Entities and Validation
- sourceEventId for charges
- invoiceId
- claimId
- receivableId

## 7. Business Rules
| ID | Rule |
|---|---|
| XWF-O2C-BR-001 | No double charge for same sourceEventId. |
| XWF-O2C-BR-002 | Discharge policy may require billing clearance. |

## 8. Approvals
Discounts/write-offs approved.

## 9. APIs and Module Ownership
**Owner:** XWF

### APIs
- `Existing APIs`

### Events Published
- `BillableEventCreated`
- `InvoiceFinalized`
- `ClaimSubmitted`
- `PaymentReceived`
- `ReceivableSettled`

### Events Consumed
- `MedicationDispensed`
- `LabResultPosted`
- `OpdEncounterClosed`
- `OtImplantUsed`
- `DischargeCompleted`

## 10. Notifications
- Denial
- High balance

## 11. Reports
- Collections
- Denial rate
- Cost-to-collect

## 12. Audit, Retention, and Privacy
Patient financial + clinical identifiers handled per privacy policy.

## 13. Failure, Idempotency, and Concurrency
- Compensating credit notes for reversed clinical events

## 14. Non-Functional Requirements
- Charge to AR visibility near-real-time

## 15. Dependencies
- HMS BIL
- FIN AR/GL/CASH

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| XWF-O2C-AC-001 | Dispense appears on bill without re-entry. |
| XWF-O2C-AC-002 | Payment reduces AR balance. |

## 17. Open Assumptions
- Package/DRG pricing iterative.

## 18. Source Traceability
Mapped from `§5.2 A; HMS billing` in `Healthcare-ERP-Pathway-and-Workflow.md`.
