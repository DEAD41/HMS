# Hire-to-Retire & Clinical Scheduling Gate

| Field | Value |
|---|---|
| Module | XWF |
| Sub-module | H2R |
| Status | Draft — pending verification |
| Source | §4.2; §8 new hire scheduling; §9 RBAC |

## 1. Scope
Ensure onboarding/credentialing gates HMS scheduling and that exit revokes access everywhere.

## 2. Exclusions
Agency staff deep marketplace.

## 3. Actors and Permissions
- HR
- Credentialing
- Security
- Clinical supervisors

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| XWF-H2R-FR-001 | Offer accept creates onboarding/employee master. |
| XWF-H2R-FR-002 | Credentials verified before clinical scheduling privileges effective. |
| XWF-H2R-FR-003 | HMS consults credential status on schedule/order sign. |
| XWF-H2R-FR-004 | Exit settles FnF, sets EmployeeExited, disables IAM, blocks roster/clinical actions. |

## 5. Workflow and State Transitions
Hired -> Credentialed -> Schedulable -> Exited/Revoked.

## 6. Data / Entities and Validation
- employeeId linkage across HRIS/IAM/HMS

## 7. Business Rules
| ID | Rule |
|---|---|
| XWF-H2R-BR-001 | Deny by default when credential status unknown/down (fail-safe configurable with break-glass). |

## 8. Approvals
Exit/termination approvals as HRIS.

## 9. APIs and Module Ownership
**Owner:** XWF

### APIs
- `Status APIs + events`

### Events Published
- `EmployeeActivated`
- `EmployeeCredentialStatusChanged`
- `EmployeeExited`
- `UserDisabled`

### Events Consumed
- `OfferAccepted`
- `CredentialExpiring`

## 10. Notifications
- Credential lapse
- Access revoke confirmation

## 11. Reports
- Credential compliance
- Access revocation lag

## 12. Audit, Retention, and Privacy
HR and access audits retained.

## 13. Failure, Idempotency, and Concurrency
- IAM disable retry until success
- HMS must re-check status, not cache forever

## 14. Non-Functional Requirements
- Revocation propagation < 5 minutes

## 15. Dependencies
- HRIS
- FND IAM
- HMS

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| XWF-H2R-AC-001 | Uncredentialed clinician cannot be scheduled. |
| XWF-H2R-AC-002 | Exited employee cannot login. |

## 17. Open Assumptions
- Fail-open emergency mode only via break-glass.

## 18. Source Traceability
Mapped from `§4.2; §8 new hire scheduling; §9 RBAC` in `Healthcare-ERP-Pathway-and-Workflow.md`.
