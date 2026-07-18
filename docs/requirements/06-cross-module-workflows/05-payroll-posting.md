# Payroll to Financials Posting

| Field | Value |
|---|---|
| Module | XWF |
| Sub-module | PAYX |
| Status | Draft — pending verification |
| Source | §4.3; §5.2 C |

## 1. Scope
Post payroll results to GL expense/liabilities and coordinate disbursement.

## 2. Exclusions
Employee reimbursement claims engine beyond payroll.

## 3. Actors and Permissions
- Payroll Officer
- Finance

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| XWF-PAYX-FR-001 | Approved payroll run publishes PayrollPosted with summarized account mappings. |
| XWF-PAYX-FR-002 | Financials creates balanced journal lines once per run. |
| XWF-PAYX-FR-003 | Bank file disbursement status updates cash/bank. |
| XWF-PAYX-FR-004 | Failures raise dead-letter and block marked 'posted' until resolved or voided. |

## 5. Workflow and State Transitions
Payroll Approved -> PayrollPosted event -> JournalPosted -> Disbursed.

## 6. Data / Entities and Validation
- payrollRunId idempotency key
- account mapping table HRIS->FIN

## 7. Business Rules
| ID | Rule |
|---|---|
| XWF-PAYX-BR-001 | Exactly-once journal per payrollRunId. |
| XWF-PAYX-BR-002 | Reversal via void workflow emits compensating journal. |

## 8. Approvals
Payroll post dual approval.

## 9. APIs and Module Ownership
**Owner:** XWF

### APIs
- `Existing APIs`

### Events Published
- `PayrollPosted`
- `JournalPosted`
- `BankFileDisbursed`

### Events Consumed
- `AttendancePosted`

## 10. Notifications
- Posting failure alerts

## 11. Reports
- Payroll vs GL reconciliation

## 12. Audit, Retention, and Privacy
Confidential payroll amounts restricted.

## 13. Failure, Idempotency, and Concurrency
- Inbox dedupe
- Mapping missing fails run post with actionable errors

## 14. Non-Functional Requirements
- Posting lag < 5s event hop; batch journal OK

## 15. Dependencies
- HRIS PAY
- FIN GL/CASH

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| XWF-PAYX-AC-001 | One payroll run creates one journal set. |
| XWF-PAYX-AC-002 | Replay does not duplicate. |

## 17. Open Assumptions
- Cost center split by assignment percentages supported.

## 18. Source Traceability
Mapped from `§4.3; §5.2 C` in `Healthcare-ERP-Pathway-and-Workflow.md`.
