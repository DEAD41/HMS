# Discharge to Insurance Claim Settlement

| Field | Value |
|---|---|
| Module | XWF |
| Sub-module | D2C |
| Status | Draft — pending verification |
| Source | §3.2 steps 8–9; §8 discharge loop |

## 1. Scope
On discharge, finalize bill, submit claim, and track AR to settlement.

## 2. Exclusions
Insurer adjudication engine internals.

## 3. Actors and Permissions
- Clinician
- Billing
- AR

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| XWF-D2C-FR-001 | Discharge completion requires configured clearances. |
| XWF-D2C-FR-002 | Final invoice produced and claim package assembled for insured patients. |
| XWF-D2C-FR-003 | FIN AR tracks claim to settlement including partials/denials. |
| XWF-D2C-FR-004 | Follow-up appointment created in HMS front office. |

## 5. Workflow and State Transitions
DischargeCompleted -> InvoiceFinalized -> ClaimSubmitted -> (Partial)Settlement.

## 6. Data / Entities and Validation
- admissionId/encounterId
- invoiceId
- claimId

## 7. Business Rules
| ID | Rule |
|---|---|
| XWF-D2C-BR-001 | Cannot lose bed release on billing retry failures—use explicit states/compensation. |
| XWF-D2C-BR-002 | Claim submission idempotent. |

## 8. Approvals
Discharge against unpaid balance waiver approvals.

## 9. APIs and Module Ownership
**Owner:** XWF

### APIs
- `Existing APIs`

### Events Published
- `DischargeCompleted`
- `InvoiceFinalized`
- `ClaimSubmitted`
- `ReceivableSettled`

### Events Consumed
- `PaymentReceived`
- `Denial`

## 10. Notifications
- Pending claim aging

## 11. Reports
- Days to claim submission
- Denial rate post-discharge

## 12. Audit, Retention, and Privacy
Clinical + financial audits linked by encounter id.

## 13. Failure, Idempotency, and Concurrency
- Saga-style state machine in discharge module
- AR sync retries

## 14. Non-Functional Requirements
- Claim draft available within minutes of discharge complete

## 15. Dependencies
- HMS DIS/BIL
- FIN AR

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| XWF-D2C-AC-001 | Insured discharge creates claim for tracking. |
| XWF-D2C-AC-002 | Settlement closes AR open item. |

## 17. Open Assumptions
- Auto e-claim format locale-specific.

## 18. Source Traceability
Mapped from `§3.2 steps 8–9; §8 discharge loop` in `Healthcare-ERP-Pathway-and-Workflow.md`.
