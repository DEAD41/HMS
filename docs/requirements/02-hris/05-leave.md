# Leave Management

| Field | Value |
|---|---|
| Module | HRIS |
| Sub-module | LVE |
| Status | Draft — pending verification |
| Source | §4.1 Leave; §4.2 step 4 |

## 1. Scope
Leave balances, requests, approvals, and roster auto-adjust signals for coverage gaps.

## 2. Exclusions
Complex union leave banking beyond configurable leave types.

## 3. Actors and Permissions
- Employee
- Manager
- HR

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HRIS-LVE-FR-001 | Maintain leave types and balances. |
| HRIS-LVE-FR-002 | Submit leave requests with date ranges. |
| HRIS-LVE-FR-003 | Route approvals and update balances on approval. |
| HRIS-LVE-FR-004 | Notify roster planners to cover gaps. |
| HRIS-LVE-FR-005 | Integrate with attendance and payroll. |

## 5. Workflow and State Transitions
LeaveRequest: `Draft -> Submitted -> Approved | Rejected | Cancelled`.

## 6. Data / Entities and Validation
- `LeaveType`
- `LeaveBalance`
- `LeaveRequest`

## 7. Business Rules
| ID | Rule |
|---|---|
| HRIS-LVE-BR-001 | Insufficient balance blocks unless unpaid/exception policy. |
| HRIS-LVE-BR-002 | Overlapping approved leave forbidden. |

## 8. Approvals
Uses FND approvals; HR override for exceptions.

## 9. APIs and Module Ownership
**Owner:** HRIS

### APIs
- `POST /api/hris/leave/requests`
- `POST /api/hris/leave/requests/{id}/cancel`
- `GET /api/hris/leave/balances/{employeeId}`

### Events Published
- `LeaveApproved`
- `LeaveRejected`
- `LeaveCancelled`

### Events Consumed
- None

## 10. Notifications
- Manager approval inbox
- Roster coverage impact

## 11. Reports
- Leave liability
- Absenteeism

## 12. Audit, Retention, and Privacy
Leave records HR confidential; retention with employment records.

## 13. Failure, Idempotency, and Concurrency
- Approval decision idempotent
- Balance update transactional

## 14. Non-Functional Requirements
- Standard API SLAs

## 15. Dependencies
- FND Approvals
- Roster
- Payroll

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HRIS-LVE-AC-001 | Approved leave reduces balance and marks attendance. |
| HRIS-LVE-AC-002 | Roster gap notification generated. |

## 17. Open Assumptions
- Calendar year vs anniversary year configurable.

## 18. Source Traceability
Mapped from `§4.1 Leave; §4.2 step 4` in `Healthcare-ERP-Pathway-and-Workflow.md`.
