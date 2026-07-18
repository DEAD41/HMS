# Billing & Claims / Insurance

| Field | Value |
|---|---|
| Module | HMS |
| Sub-module | BIL |
| Status | Draft — pending verification |
| Source | §3.1 Billing & claims; §3.2 steps 7–9; §3.3 billable events -> Financials |

## 1. Scope
Real-time charge accumulation, patient billing, insurance claim package assembly, and handoff to Financials AR.

## 2. Exclusions
Insurer portal replacement; complex national DRG grouper beyond configurable packages initially.

## 3. Actors and Permissions
- Billing Officer
- Cashier
- Insurance/TPA Desk
- Finance AR (consumer)

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HMS-BIL-FR-001 | Accumulate charges from consultation, diagnostics, pharmacy, bed, OT, nursing, and other services in real time. |
| HMS-BIL-FR-002 | Generate invoices split between self-pay and insurance/TPA portions. |
| HMS-BIL-FR-003 | Assemble claim packages for TPA/insurer submission. |
| HMS-BIL-FR-004 | Record payments/co-pay at cashier and emit AR events. |
| HMS-BIL-FR-005 | Support discounts/waivers under approval policy. |
| HMS-BIL-FR-006 | Track claim status updates toward settlement with Financials. |

## 5. Workflow and State Transitions
Bill: `Open -> Interim -> Finalized -> PartiallyPaid -> Paid | WrittenOff`.
Claim: `Draft -> Submitted -> Accepted | PartiallyPaid | Denied -> Appealed -> Settled`.

## 6. Data / Entities and Validation
- `Charge`
- `Invoice`
- `InvoiceLine`
- `Claim`
- `ClaimLine`
- `PaymentReceipt`

## 7. Business Rules
| ID | Rule |
|---|---|
| HMS-BIL-BR-001 | Every charge references patient, encounter, charge code, amount, taxes, cost center. |
| HMS-BIL-BR-002 | Finalization blocked if mandatory coding missing when policy requires. |
| HMS-BIL-BR-003 | Billable events must be idempotent to prevent double charging. |

## 8. Approvals
Discounts above threshold and write-offs require approval via FND engine.

## 9. APIs and Module Ownership
**Owner:** HMS

### APIs
- `POST /api/hms/billing/charges`
- `POST /api/hms/billing/invoices/{id}/finalize`
- `POST /api/hms/billing/claims`
- `POST /api/hms/billing/payments`

### Events Published
- `BillableEventCreated`
- `InvoiceFinalized`
- `ClaimSubmitted`
- `PaymentReceived`

### Events Consumed
- `MedicationDispensed`
- `LabResultPosted`
- `OtImplantUsed`
- `PatientAdmitted`
- `OpdEncounterClosed`

## 10. Notifications
- Denial alerts
- High-balance alerts

## 11. Reports
- Daily collections
- Claim aging (ops)
- Charge mix

## 12. Audit, Retention, and Privacy
Financial artifacts retained per statutory policy; access restricted; payment voids audited.

## 13. Failure, Idempotency, and Concurrency
- Charge posting idempotent by sourceEventId.
- Payment allocation concurrency safe.

## 14. Non-Functional Requirements
- Charge post P95 < 300ms

## 15. Dependencies
- FIN AR/GL
- FND Approvals
- All HMS charge sources

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HMS-BIL-AC-001 | Pharmacy dispense creates charge without manual re-entry. |
| HMS-BIL-AC-002 | Final invoice split self-pay vs insurance correctly. |
| HMS-BIL-AC-003 | Payment posts receivable update in Financials. |

## 17. Open Assumptions
- Tax rules localized via FIN tax configuration.

## 18. Source Traceability
Mapped from `§3.1 Billing & claims; §3.2 steps 7–9; §3.3 billable events -> Financials` in `Healthcare-ERP-Pathway-and-Workflow.md`.
