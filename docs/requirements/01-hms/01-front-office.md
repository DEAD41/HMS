# Front Office — Registration, Appointments, Insurance/TPA

| Field | Value |
|---|---|
| Module | HMS |
| Sub-module | FO |
| Status | Draft — pending verification |
| Source | §3.1 Front office; §3.2 steps 1,9 |

## 1. Scope
Patient registration (new/returning), appointment scheduling, and insurance/TPA eligibility verification.

## 2. Exclusions
Full insurer adjudication engine (claims belong with billing); CRM marketing.

## 3. Actors and Permissions
- Front Desk Officer
- Insurance Desk
- Patient (portal booking — Phase 4)
- Scheduling Supervisor

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HMS-FO-FR-001 | Register new patients into patient master with demographics and identifiers. |
| HMS-FO-FR-002 | Match returning patients to avoid duplicates using configurable match rules. |
| HMS-FO-FR-003 | Schedule, reschedule, and cancel appointments against providers and clinics. |
| HMS-FO-FR-004 | Verify insurance/TPA eligibility and capture coverage snapshot for the visit. |
| HMS-FO-FR-005 | Capture referral source and visit reason. |
| HMS-FO-FR-006 | Support walk-in queue tickets linked to OPD/Emergency routing. |

## 5. Workflow and State Transitions
Patient: `Active | Merged | Inactive`.
Appointment: `Scheduled -> CheckedIn -> InProgress -> Completed | Cancelled | NoShow`.
Eligibility check: `NotChecked -> Verified | Pending | Failed`.

## 6. Data / Entities and Validation
- `Patient`, `PatientIdentifier`, `Appointment`, `InsurancePolicy`, `EligibilityCheck`
- Validation: names required; DOB; at least one phone/ID per facility policy; appointment slot conflicts prevented per provider

## 7. Business Rules
| ID | Rule |
|---|---|
| HMS-FO-BR-001 | Duplicate patients are merged via controlled merge with audit, not hard-deleted. |
| HMS-FO-BR-002 | Appointment with clinician requires clinician active + credential OK from HRIS gate. |
| HMS-FO-BR-003 | Eligibility failure can soft-block or warn based on facility policy. |

## 8. Approvals
Patient merge and large appointment template changes may require supervisor approval.

## 9. APIs and Module Ownership
**Owner:** HMS

### APIs
- `POST /api/hms/patients`
- `GET /api/hms/patients/{id}`
- `POST /api/hms/appointments`
- `POST /api/hms/insurance/eligibility-checks`

### Events Published
- `PatientChanged`
- `AppointmentScheduled`
- `AppointmentCheckedIn`
- `EligibilityVerified`

### Events Consumed
- `EmployeeCredentialStatusChanged`

## 10. Notifications
- Appointment reminders
- Eligibility failure to insurance desk

## 11. Reports
- Daily appointment list
- Registration volume
- Insurance verification turnaround

## 12. Audit, Retention, and Privacy
Patient demographics are PHI. Access audited. Retention per clinical records policy.

## 13. Failure, Idempotency, and Concurrency
- Registration API idempotent by requestId.
- Double-booking prevented with transactional slot lock.

## 14. Non-Functional Requirements
- Search patient P95 < 300ms
- Support high front-desk concurrency at opening hours

## 15. Dependencies
- FND IAM/Tenancy
- HRIS credentials for provider scheduling
- FIN payer refs optional

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HMS-FO-AC-001 | New patient registration creates selectable patient master record. |
| HMS-FO-AC-002 | Cannot schedule inactive/unlicensed clinician. |
| HMS-FO-AC-003 | Checked-in appointment is available to OPD worklist. |

## 17. Open Assumptions
- Default ID types configurable (CNIC/MRN/passport/etc.).

## 18. Source Traceability
Mapped from `§3.1 Front office; §3.2 steps 1,9` in `Healthcare-ERP-Pathway-and-Workflow.md`.
