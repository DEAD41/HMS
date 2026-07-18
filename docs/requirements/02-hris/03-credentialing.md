# Credentialing & Clinical Privileges

| Field | Value |
|---|---|
| Module | HRIS |
| Sub-module | CRD |
| Status | Draft — pending verification |
| Source | §4.1 credentialing; §4.2 steps 2,6; §4.3 gates HMS |

## 1. Scope
Track licenses, certifications, specialty privileges, expiry alerts, and clinical action gating signals.

## 2. Exclusions
External medical council live verification APIs beyond manual evidence.

## 3. Actors and Permissions
- Credentialing Officer
- Medical Director
- Clinician

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HRIS-CRD-FR-001 | Record licenses/certifications with issue/expiry dates and evidence documents. |
| HRIS-CRD-FR-002 | Maintain specialty privilege grants per facility. |
| HRIS-CRD-FR-003 | Emit credential status changes for HMS scheduling/order signing gates. |
| HRIS-CRD-FR-004 | Alert before expiry and auto-suspend privileges on lapse per policy. |
| HRIS-CRD-FR-005 | Support temporary privilege grants with end dates. |

## 5. Workflow and State Transitions
Credential: `Submitted -> Verified -> Active -> ExpiringSoon -> Expired | Suspended | Revoked`.

## 6. Data / Entities and Validation
- `Credential`
- `Privilege`
- `CredentialAlert`

## 7. Business Rules
| ID | Rule |
|---|---|
| HRIS-CRD-BR-001 | HMS must deny schedule/sign when required credential inactive. |
| HRIS-CRD-BR-002 | Expired credential cannot be used even if employee active. |

## 8. Approvals
Privilege grant/revoke for high-risk procedures require Medical Director approval.

## 9. APIs and Module Ownership
**Owner:** HRIS

### APIs
- `POST /api/hris/credentials`
- `POST /api/hris/privileges`
- `GET /api/hris/credentials/status/{employeeId}`

### Events Published
- `EmployeeCredentialStatusChanged`
- `CredentialExpiring`

### Events Consumed
- None

## 10. Notifications
- Expiry alerts to clinician and credentialing office

## 11. Reports
- Expiring credentials
- Privilege matrix

## 12. Audit, Retention, and Privacy
Credential evidence retained; changes audited immutable.

## 13. Failure, Idempotency, and Concurrency
- Status recompute job idempotent
- Concurrent privilege edits conflict-checked

## 14. Non-Functional Requirements
- Status check API P95 < 50ms cached

## 15. Dependencies
- HRIS Employee
- HMS consumers
- FND Notifications/Docs

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HRIS-CRD-AC-001 | Lapsed license sets credential status inactive and HMS blocks sign-off. |
| HRIS-CRD-AC-002 | Expiry alert fires within configured lead time. |

## 17. Open Assumptions
- Lead time default 30/60/90 days configurable.

## 18. Source Traceability
Mapped from `§4.1 credentialing; §4.2 steps 2,6; §4.3 gates HMS` in `Healthcare-ERP-Pathway-and-Workflow.md`.
