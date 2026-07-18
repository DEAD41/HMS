# Emergency & Triage

| Field | Value |
|---|---|
| Module | HMS |
| Sub-module | ER |
| Status | Draft — pending verification |
| Source | §3.1 Emergency; §3.2 step 2 |

## 1. Scope
Triage assessment, emergency encounter management, and routing to OPD/IPD/OT as needed.

## 2. Exclusions
Ambulance fleet management; disaster external command systems.

## 3. Actors and Permissions
- Triage Nurse
- ER Physician
- ER Clerk

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HMS-ER-FR-001 | Register/identify emergency patient rapidly (including unidentified patient workflow). |
| HMS-ER-FR-002 | Capture triage score/category and vitals. |
| HMS-ER-FR-003 | Track ER encounter timeline and interventions. |
| HMS-ER-FR-004 | Route to admission, OT, or discharge from ER. |
| HMS-ER-FR-005 | Support emergency override for credential/payment soft-blocks with audit. |

## 5. Workflow and State Transitions
Triage: `Arrived -> Triaged -> InTreatment -> Disposed`.
Disposition: `Discharge | AdmitIPD | Transfer | Deceased | LAMA`.

## 6. Data / Entities and Validation
- `ErEncounter`
- `TriageAssessment`
- unidentified patient temporary IDs

## 7. Business Rules
| ID | Rule |
|---|---|
| HMS-ER-BR-001 | Critical triage category gets queue prioritization. |
| HMS-ER-BR-002 | Unidentified patients can receive orders; identity merge later. |

## 8. Approvals
Emergency break-glass clinical access uses FND IAM break-glass with reason.

## 9. APIs and Module Ownership
**Owner:** HMS

### APIs
- `POST /api/hms/er/encounters`
- `POST /api/hms/er/encounters/{id}/triage`
- `POST /api/hms/er/encounters/{id}/dispose`

### Events Published
- `ErEncounterOpened`
- `PatientTriaged`
- `ErDisposed`

### Events Consumed
- `EmployeeCredentialStatusChanged`

## 10. Notifications
- Critical triage alerts to ER team

## 11. Reports
- ER wait times
- Triage category mix

## 12. Audit, Retention, and Privacy
ER records PHI; high audit scrutiny on overrides.

## 13. Failure, Idempotency, and Concurrency
- Unidentified ID generation unique
- Disposition idempotent

## 14. Non-Functional Requirements
- Triage board real-time updates

## 15. Dependencies
- HMS Front Office/IPD/OT/Billing
- FND IAM

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HMS-ER-AC-001 | Unidentified patient can be created in <60 seconds path. |
| HMS-ER-AC-002 | Admit disposition creates IPD admission request. |

## 17. Open Assumptions
- Triage scale configurable (e.g., ESI/local).

## 18. Source Traceability
Mapped from `§3.1 Emergency; §3.2 step 2` in `Healthcare-ERP-Pathway-and-Workflow.md`.
