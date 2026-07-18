# Medical Records (EMR/EHR)

| Field | Value |
|---|---|
| Module | HMS |
| Sub-module | EMR |
| Status | Draft — pending verification |
| Source | §3.1 Medical Records; §3.2 clinical orders hub |

## 1. Scope
Longitudinal patient chart, clinical documentation, order entry, results inbox, and care timeline.

## 2. Exclusions
Population health research warehouse; full FHIR external ecosystem in later phases.

## 3. Actors and Permissions
- Clinicians
- Clinical Coders
- Medical Records Officer
- Nurses

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HMS-EMR-FR-001 | Maintain longitudinal chart across OPD/IPD/ER/OT encounters. |
| HMS-EMR-FR-002 | Support structured and narrative clinical notes with sign/amend. |
| HMS-EMR-FR-003 | Provide CPOE for labs, radiology, medications, procedures. |
| HMS-EMR-FR-004 | Display results/reports posted from LIS/RIS and dispense summaries. |
| HMS-EMR-FR-005 | Enforce credential gates on order sign and note sign. |
| HMS-EMR-FR-006 | Support problem list, allergies, and diagnosis coding entries. |

## 5. Workflow and State Transitions
Note: `Draft -> Signed -> Amended`.
Order: `Draft -> Signed -> InFulfillment -> Completed | Cancelled`.

## 6. Data / Entities and Validation
- `ClinicalNote`
- `ClinicalOrder`
- `Allergy`
- `Problem`
- `EncounterChart` projection

## 7. Business Rules
| ID | Rule |
|---|---|
| HMS-EMR-BR-001 | Signed notes are immutable; corrections via amendment. |
| HMS-EMR-BR-002 | Allergy hard-stop/warn on medication order per severity policy. |
| HMS-EMR-BR-003 | Orders require patient encounter context. |

## 8. Approvals
Break-glass chart access uses FND IAM policy.

## 9. APIs and Module Ownership
**Owner:** HMS

### APIs
- `POST /api/hms/emr/notes`
- `POST /api/hms/emr/notes/{id}/sign`
- `POST /api/hms/emr/orders`
- `GET /api/hms/emr/chart/{patientId}`

### Events Published
- `ClinicalNoteSigned`
- `ClinicalOrderPlaced`
- `ClinicalOrderCancelled`

### Events Consumed
- `LabResultPosted`
- `RadiologyReportPosted`
- `MedicationDispensed`
- `EmployeeCredentialStatusChanged`

## 10. Notifications
- Critical results
- Unsigned draft aging for clinicians

## 11. Reports
- Chart access log
- Order volume by type

## 12. Audit, Retention, and Privacy
EMR is primary clinical system of record; strict PHI controls; amendment history preserved.

## 13. Failure, Idempotency, and Concurrency
- Note sign concurrency safe
- Order sign idempotent

## 14. Non-Functional Requirements
- Chart summary load P95 < 1s for recent encounters

## 15. Dependencies
- All HMS clinical sub-modules
- HRIS credentials
- FND docs for attachments

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HMS-EMR-AC-001 | Signed lab order appears in LIS worklist. |
| HMS-EMR-AC-002 | Lapsed clinician credential blocks new order sign. |

## 17. Open Assumptions
- FHIR export optional later; internal API first.

## 18. Source Traceability
Mapped from `§3.1 Medical Records; §3.2 clinical orders hub` in `Healthcare-ERP-Pathway-and-Workflow.md`.
