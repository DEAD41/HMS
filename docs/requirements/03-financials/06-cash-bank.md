# Cash & Bank Management

| Field | Value |
|---|---|
| Module | FIN |
| Sub-module | CASH |
| Status | Draft — pending verification |
| Source | §5.1 Cash & bank |

## 1. Scope
Cash drawers, bank accounts, deposits, reconciliations, and disbursement execution records.

## 2. Exclusions
Full TMS / multi-bank connectivity suite.

## 3. Actors and Permissions
- Cashier Supervisor
- Treasury Accountant

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| FIN-CASH-FR-001 | Maintain bank/cash accounts. |
| FIN-CASH-FR-002 | Record deposits and withdrawals. |
| FIN-CASH-FR-003 | Reconcile bank statements. |
| FIN-CASH-FR-004 | Integrate disbursement confirmations for AP/payroll files. |

## 5. Workflow and State Transitions
BankRec: `Open -> InProgress -> Reconciled`.
CashSession: `Open -> Closed`.

## 6. Data / Entities and Validation
- `BankAccount`
- `CashSession`
- `BankStatement`
- `BankReconciliation`

## 7. Business Rules
| ID | Rule |
|---|---|
| FIN-CASH-BR-001 | Cash session must close balanced per policy. |
| FIN-CASH-BR-002 | Reconciled items immutable. |

## 8. Approvals
Manual bank adjustments require approval above threshold.

## 9. APIs and Module Ownership
**Owner:** FIN

### APIs
- `POST /api/fin/cash/sessions`
- `POST /api/fin/bank/statements/import`
- `POST /api/fin/bank/reconciliations`

### Events Published
- `BankReconciliationCompleted`
- `CashSessionClosed`

### Events Consumed
- `ApPaymentDisbursed`
- `PaymentReceived`
- `PayrollPosted`

## 10. Notifications
- Unreconciled item aging alerts

## 11. Reports
- Cash position
- Reconciliation status

## 12. Audit, Retention, and Privacy
Banking data sensitive; dual control recommended for disbursements.

## 13. Failure, Idempotency, and Concurrency
- Import idempotent by statement fingerprint

## 14. Non-Functional Requirements
- Import 10k lines within batch SLA

## 15. Dependencies
- FIN AP/AR/Payroll

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| FIN-CASH-AC-001 | Cashier receipt can be deposited and reconciled. |
| FIN-CASH-AC-002 | Payroll bank file disbursement status trackable. |

## 17. Open Assumptions
- Direct bank API optional.

## 18. Source Traceability
Mapped from `§5.1 Cash & bank` in `Healthcare-ERP-Pathway-and-Workflow.md`.
