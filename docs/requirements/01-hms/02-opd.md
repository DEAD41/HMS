# Outpatient Department (OPD)

| Field | Value |
|---|---|
| Module | HMS |
| Sub-module | OPD |
| Status | Draft — pending verification |
| Source | §3.1 OPD; §3.2 steps 2–4 |

## 1. Scope
Manage outpatient consultation encounters, vitals, clinical notes handoff to EMR, and order placement.

## 2. Exclusions
Full inpatient nursing; long-stay billing specifics.

## 3. Actors and Permissions
- OPD Physician
- OPD Nurse
- OPD Clerk

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HMS-OPD-FR-001 | Create OPD encounter from checked-in appointment or walk-in. |
| HMS-OPD-FR-002 | Record vitals and chief complaint. |
| HMS-OPD-FR-003 | Allow clinician to document assessment/plan via EMR integration. |
| HMS-OPD-FR-004 | Place lab/radiology/medication/procedure orders from encounter. |
| HMS-OPD-FR-005 | Close encounter with disposition (home, admit, refer ER, follow-up). |
| HMS-OPD-FR-006 | Post consultation charges to billing. |

## 5. Workflow and State Transitions
Encounter: `Open -> InConsultation -> AwaitingOrders -> Closed | Cancelled`.
Disposition recorded on close.

## 6. Data / Entities and Validation
- `OpdEncounter`, `VitalSigns`, link to `ClinicalOrder`s and EMR note ids

## 7. Business Rules
| ID | Rule |
|---|---|
| HMS-OPD-BR-001 | Only credentialed clinicians can sign consultation notes/orders. |
| HMS-OPD-BR-002 | Closing encounter with unsigned mandatory notes blocked if policy requires. |
| HMS-OPD-BR-003 | Admit disposition starts IPD admission workflow. |

## 8. Approvals
Encounter cancellation after charges may require billing supervisor approval.

## 9. APIs and Module Ownership
**Owner:** HMS

### APIs
- `POST /api/hms/opd/encounters`
- `POST /api/hms/opd/encounters/{id}/vitals`
- `POST /api/hms/opd/encounters/{id}/close`

### Events Published
- `OpdEncounterOpened`
- `OpdEncounterClosed`
- `ClinicalOrderPlaced`

### Events Consumed
- `LabResultPosted`
- `RadiologyReportPosted`
- `MedicationDispensed`

## 10. Notifications
- Nurse alert for pending vitals
- Physician alert for critical results

## 11. Reports
- OPD volume by clinic
- Average consultation time

## 12. Audit, Retention, and Privacy
Clinical documentation PHI; signed note amendments audited.

## 13. Failure, Idempotency, and Concurrency
- Concurrent note edits use optimistic concurrency
- Order place idempotent

## 14. Non-Functional Requirements
- Worklist refresh under 2s

## 15. Dependencies
- HMS Front Office
- HMS EMR
- HRIS credentials
- FIN billing events

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HMS-OPD-AC-001 | Checked-in patient appears on physician worklist. |
| HMS-OPD-AC-002 | Signed order creates fulfillment workitem in LIS/RIS/Pharmacy. |
| HMS-OPD-AC-003 | Consultation fee appears on patient bill. |

## 17. Open Assumptions
- OPD charge master codes maintained in billing configuration.

## 18. Source Traceability
Mapped from `§3.1 OPD; §3.2 steps 2–4` in `Healthcare-ERP-Pathway-and-Workflow.md`.
