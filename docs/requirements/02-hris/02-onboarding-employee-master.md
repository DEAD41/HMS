# Onboarding & Employee Master

| Field | Value |
|---|---|
| Module | HRIS |
| Sub-module | EMP |
| Status | Draft — pending verification |
| Source | §4.1 Employee master; §4.2 step 2; §2 employee ownership |

## 1. Scope
Create and maintain employee master, documents, department assignment, and user provisioning trigger.

## 2. Exclusions
Full LMS content platform.

## 3. Actors and Permissions
- HR Officer
- Department Head
- Employee

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HRIS-EMP-FR-001 | Create employee master from hired candidate or direct hire. |
| HRIS-EMP-FR-002 | Capture demographics, employment terms, department, cost center, reporting manager. |
| HRIS-EMP-FR-003 | Collect onboarding documents via document vault. |
| HRIS-EMP-FR-004 | Activate employee and emit EmployeeChanged for projections/IAM linking. |
| HRIS-EMP-FR-005 | Support transfers and status changes. |

## 5. Workflow and State Transitions
Employee: `Onboarding -> Active -> Suspended -> Exited -> Archived`.

## 6. Data / Entities and Validation
- `Employee`
- `EmploymentContract`
- `EmployeeDocumentLink`
- `OrgAssignment`

## 7. Business Rules
| ID | Rule |
|---|---|
| HRIS-EMP-BR-001 | Employee code unique per tenant. |
| HRIS-EMP-BR-002 | Active clinical staff must eventually have credential records before scheduling. |
| HRIS-EMP-BR-003 | Cost center required before payroll finalize. |

## 8. Approvals
Backdated join date corrections require HR Manager approval.

## 9. APIs and Module Ownership
**Owner:** HRIS

### APIs
- `POST /api/hris/employees`
- `PUT /api/hris/employees/{id}`
- `POST /api/hris/employees/{id}/activate`

### Events Published
- `EmployeeChanged`
- `EmployeeActivated`

### Events Consumed
- `OfferAccepted`
- `DocumentAvailable`

## 10. Notifications
- Missing onboarding document reminders

## 11. Reports
- Headcount by department

## 12. Audit, Retention, and Privacy
Employee PII/HR confidential; access role-restricted; audited.

## 13. Failure, Idempotency, and Concurrency
- Activate idempotent
- Optimistic concurrency on employee

## 14. Non-Functional Requirements
- Employee search P95 < 300ms

## 15. Dependencies
- FND Docs/IAM
- FIN cost centers

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HRIS-EMP-AC-001 | Activated employee appears in master projections. |
| HRIS-EMP-AC-002 | IAM can link user to employee id. |

## 17. Open Assumptions
- Biometric enrollment system external.

## 18. Source Traceability
Mapped from `§4.1 Employee master; §4.2 step 2; §2 employee ownership` in `Healthcare-ERP-Pathway-and-Workflow.md`.
