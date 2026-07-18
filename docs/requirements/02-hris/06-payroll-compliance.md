# Payroll & Statutory Compliance

| Field | Value |
|---|---|
| Module | HRIS |
| Sub-module | PAY |
| Status | Draft — pending verification |
| Source | §4.1 Payroll; §4.2 step 5; §4.3 posts to Financials |

## 1. Scope
Monthly payroll processing from attendance/leave/earnings/deductions and posting salary expense/liabilities to Financials with bank file generation.

## 2. Exclusions
Full treasury bank host-to-host beyond payment file; multi-country statutory packs beyond configured locale pack.

## 3. Actors and Permissions
- Payroll Officer
- Finance Controller
- HR Manager

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HRIS-PAY-FR-001 | Configure earnings/deductions and statutory rules pack. |
| HRIS-PAY-FR-002 | Run payroll calculation for a period. |
| HRIS-PAY-FR-003 | Support review adjustments and approvals. |
| HRIS-PAY-FR-004 | Finalize payroll and post accounting entries to Financials. |
| HRIS-PAY-FR-005 | Generate bank disbursement file and payslips. |

## 5. Workflow and State Transitions
PayrollRun: `Open -> Calculated -> InReview -> Approved -> Posted | Void`.

## 6. Data / Entities and Validation
- `PayrollRun`
- `Payslip`
- `PayrollPosting`
- `BankFile`

## 7. Business Rules
| ID | Rule |
|---|---|
| HRIS-PAY-BR-001 | Cannot modify posted run except via reversal/void workflow. |
| HRIS-PAY-BR-002 | Employee without cost center excluded from finalize with error list. |

## 8. Approvals
Payroll approve/post requires Finance/HR dual approval per policy.

## 9. APIs and Module Ownership
**Owner:** HRIS

### APIs
- `POST /api/hris/payroll/runs`
- `POST /api/hris/payroll/runs/{id}/calculate`
- `POST /api/hris/payroll/runs/{id}/post`

### Events Published
- `PayrollPosted`
- `PayslipPublished`

### Events Consumed
- `AttendancePosted`
- `LeaveApproved`

## 10. Notifications
- Payslip available
- Posting failure alerts

## 11. Reports
- Payroll register
- Statutory summaries
- Variance vs prior period

## 12. Audit, Retention, and Privacy
Payroll data highly confidential; access tightly controlled; statutory retention.

## 13. Failure, Idempotency, and Concurrency
- Posting uses outbox; financial consumer idempotent by payrollRunId
- Calculate re-runnible before approve

## 14. Non-Functional Requirements
- Calculate 2,000 employees within configured batch SLA

## 15. Dependencies
- FIN GL
- FND Approvals
- Attendance/Leave

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HRIS-PAY-AC-001 | Posted payroll creates GL expense/liability entries once. |
| HRIS-PAY-AC-002 | Bank file generated for approved net pay. |

## 17. Open Assumptions
- Statutory pack initially for primary deployment country.

## 18. Source Traceability
Mapped from `§4.1 Payroll; §4.2 step 5; §4.3 posts to Financials` in `Healthcare-ERP-Pathway-and-Workflow.md`.
