# Employee Self-Service Portal

| Field | Value |
|---|---|
| Module | HRIS |
| Sub-module | ESS |
| Status | Draft — pending verification |
| Source | §4.1 ESS |

## 1. Scope
Employee self-service for profile view, leave, payslips, roster, and training assignments.

## 2. Exclusions
Patient portal (HMS); vendor portal (Procurement).

## 3. Actors and Permissions
- Employee

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HRIS-ESS-FR-001 | View personal profile and documents metadata. |
| HRIS-ESS-FR-002 | Submit leave and view balances. |
| HRIS-ESS-FR-003 | View published roster and payslips. |
| HRIS-ESS-FR-004 | Update limited personal contacts with verification rules. |

## 5. Workflow and State Transitions
ESS actions reuse underlying entity states.

## 6. Data / Entities and Validation
- No new masters; facade over HRIS services

## 7. Business Rules
| ID | Rule |
|---|---|
| HRIS-ESS-BR-001 | Employees only see own data unless manager delegation features enabled. |

## 8. Approvals
Sensitive profile changes may require HR approval.

## 9. APIs and Module Ownership
**Owner:** HRIS

### APIs
- `GET /api/hris/ess/me`
- `POST /api/hris/ess/leave`
- `GET /api/hris/ess/payslips`

### Events Published
- None

### Events Consumed
- `PayslipPublished`
- `RosterPublished`

## 10. Notifications
- Leave status changes

## 11. Reports
- ESS adoption metrics

## 12. Audit, Retention, and Privacy
Same controls as source data; authentication required.

## 13. Failure, Idempotency, and Concurrency
- Standard idempotency on submissions

## 14. Non-Functional Requirements
- Mobile-responsive UI target

## 15. Dependencies
- Leave/Payroll/Roster APIs

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HRIS-ESS-AC-001 | Employee can download own payslip after publish. |
| HRIS-ESS-AC-002 | Cannot view another employee's payslip. |

## 17. Open Assumptions
- Mobile native apps later.

## 18. Source Traceability
Mapped from `§4.1 ESS` in `Healthcare-ERP-Pathway-and-Workflow.md`.
