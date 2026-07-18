# Identity & RBAC

| Field | Value |
|---|---|
| Module | FND |
| Sub-module | IAM |
| Status | Draft — pending verification |
| Source | §9 Governance — Role-based access control |

## 1. Scope
Single identity and role model governing access across HMS, HRIS, Financials, Inventory, and Procurement, sourced from HRIS employee linkage where applicable.

## 2. Exclusions
External IdP federation beyond OIDC in Phase 1; advanced ABAC policies in Phase 4.

## 3. Actors and Permissions
- Security Admin — manage roles/permissions
- All users — authenticate and act within grants
- Service accounts — module-to-module internal calls

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| FND-IAM-FR-001 | System shall authenticate users via secure token-based auth (OIDC-compatible). |
| FND-IAM-FR-002 | Every API authorization check shall evaluate role permissions and facility scope. |
| FND-IAM-FR-003 | Roles shall be composable permission sets assignable per facility. |
| FND-IAM-FR-004 | Employee-linked users shall inherit employment status gates from HRIS (active/exited). |
| FND-IAM-FR-005 | Privileged clinical actions shall optionally require credential checks via HRIS integration. |
| FND-IAM-FR-006 | Failed authorization attempts shall be logged without leaking sensitive resource details. |
| FND-IAM-FR-007 | Break-glass emergency access shall be supported with mandatory reason and heightened audit. |

## 5. Workflow and State Transitions
User lifecycle: `Invited -> Active -> Locked -> Disabled`.
Role assignment: `PendingApproval(optional) -> Active -> Revoked`.

## 6. Data / Entities and Validation
- `User`, `Role`, `Permission`, `UserRoleAssignment`, `FacilityScope`
- Permission codes namespaced by module, e.g. `HMS.Patient.Register`
- Password/secret storage never in application DB when external IdP used

## 7. Business Rules
| ID | Rule |
|---|---|
| FND-IAM-BR-001 | Disabled/exited employees cannot authenticate except break-glass accounts. |
| FND-IAM-BR-002 | Permission checks are deny-by-default. |
| FND-IAM-BR-003 | A user may hold different roles in different facilities. |

## 8. Approvals
Role creation and privileged role assignment require Security Admin approval workflow.

## 9. APIs and Module Ownership
**Owner:** FND

### APIs
- `POST /api/fnd/auth/login (or external IdP)`
- `GET/POST /api/fnd/roles`
- `POST /api/fnd/users/{id}/roles`
- `GET /api/fnd/me`

### Events Published
- `UserDisabled`
- `RoleAssignmentChanged`

### Events Consumed
- `EmployeeExited`
- `EmployeeCredentialStatusChanged`

## 10. Notifications
- Notify user on lockout
- Notify Security Admin on break-glass use

## 11. Reports
- Role matrix
- Access review report

## 12. Audit, Retention, and Privacy
Immutable security audit for login, logout, failures, role changes, break-glass. Retention minimum 7 years.

## 13. Failure, Idempotency, and Concurrency
- Token replay protection via jti/expiry.
- Concurrent role changes take effect on next authorization check.
- Idempotent role assignment APIs.

## 14. Non-Functional Requirements
- Authorization decision overhead P95 < 20ms cached.
- Support 5,000 concurrent authenticated users per deployment target.

## 15. Dependencies
- FND Tenancy
- HRIS employee status/credentials
- FND Audit

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| FND-IAM-AC-001 | User without permission cannot access protected endpoint (403). |
| FND-IAM-AC-002 | Exited employee user is blocked at next request. |
| FND-IAM-AC-003 | Break-glass access is fully audited with reason. |

## 17. Open Assumptions
- Initial auth may use built-in Identity with migration path to external IdP.
- Permission catalog is code-defined and seeded.

## 18. Source Traceability
Mapped from `§9 Governance — Role-based access control` in `Healthcare-ERP-Pathway-and-Workflow.md`.
