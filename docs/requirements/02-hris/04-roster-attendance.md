# Duty Roster, Shifts & Attendance

| Field | Value |
|---|---|
| Module | HRIS |
| Sub-module | ROS |
| Status | Draft — pending verification |
| Source | §4.1 Attendance/roster; §4.2 step 3 |

## 1. Scope
Build department shift rosters (nursing/ICU/OT coverage) and capture attendance for payroll.

## 2. Exclusions
Advanced predictive staffing AI.

## 3. Actors and Permissions
- Roster Planner
- Nursing Supervisor
- Employees
- Payroll Officer (read)

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HRIS-ROS-FR-001 | Create shift templates and period rosters by department/ward. |
| HRIS-ROS-FR-002 | Detect coverage gaps and skill/credential mismatches. |
| HRIS-ROS-FR-003 | Capture attendance (manual/biometric import). |
| HRIS-ROS-FR-004 | Publish roster to employees and HMS clinical scheduling consumers. |
| HRIS-ROS-FR-005 | Lock roster periods for payroll. |

## 5. Workflow and State Transitions
RosterPeriod: `Draft -> Published -> Locked`.
Attendance: `Present | Absent | HalfDay | OnLeave | Holiday`.

## 6. Data / Entities and Validation
- `ShiftTemplate`
- `RosterAssignment`
- `AttendanceRecord`

## 7. Business Rules
| ID | Rule |
|---|---|
| HRIS-ROS-BR-001 | Cannot assign clinician lacking required credential for unit. |
| HRIS-ROS-BR-002 | Locked period attendance corrections require approval. |

## 8. Approvals
Published roster changes within 24h may require supervisor approval.

## 9. APIs and Module Ownership
**Owner:** HRIS

### APIs
- `POST /api/hris/rosters`
- `POST /api/hris/rosters/{id}/publish`
- `POST /api/hris/attendance`

### Events Published
- `RosterPublished`
- `AttendancePosted`

### Events Consumed
- `EmployeeCredentialStatusChanged`
- `LeaveApproved`

## 10. Notifications
- Coverage gap alerts

## 11. Reports
- Coverage compliance
- Overtime preview

## 12. Audit, Retention, and Privacy
Attendance feeds payroll; corrections audited.

## 13. Failure, Idempotency, and Concurrency
- Publish conflict detection
- Attendance upsert idempotent by employee/date/source

## 14. Non-Functional Requirements
- Roster publish for 500 staff < 5s

## 15. Dependencies
- HRIS Leave/Credentials
- HMS scheduling
- Payroll

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HRIS-ROS-AC-001 | Publishing roster with unqualified ICU nurse fails validation. |
| HRIS-ROS-AC-002 | Attendance available to payroll run. |

## 17. Open Assumptions
- Biometric devices integrate via import file/API adapter.

## 18. Source Traceability
Mapped from `§4.1 Attendance/roster; §4.2 step 3` in `Healthcare-ERP-Pathway-and-Workflow.md`.
