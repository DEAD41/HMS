# IPD / Bed Management / Nursing

| Field | Value |
|---|---|
| Module | HMS |
| Sub-module | IPD |
| Status | Draft — pending verification |
| Source | §3.1 IPD; §3.2 steps 5 |

## 1. Scope
Admissions, bed allocation, nursing care plans, daily MAR, and per-bed consumable tracking.

## 2. Exclusions
Home-care episodes; external referral hospital bed network.

## 3. Actors and Permissions
- Admission Desk
- Ward Nurse
- Nursing Supervisor
- Attending Physician
- Bed Management

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HMS-IPD-FR-001 | Admit patient to IPD with admitting diagnosis and attending clinician. |
| HMS-IPD-FR-002 | Allocate/transfer beds with occupancy integrity. |
| HMS-IPD-FR-003 | Maintain nursing care plan and shift handover notes. |
| HMS-IPD-FR-004 | Record medication administration (MAR) against pharmacy-dispensed orders. |
| HMS-IPD-FR-005 | Track consumables issued to patient/bed and post usage. |
| HMS-IPD-FR-006 | Capture daily ward charges automatically based on bed class. |

## 5. Workflow and State Transitions
Admission: `Requested -> Admitted -> Transferred -> DischargeInitiated -> Discharged`.
Bed: `Available -> Occupied -> Blocked -> Maintenance`.
MAR dose: `Due -> Administered | Held | Refused | Missed`.

## 6. Data / Entities and Validation
- `Admission`, `Bed`, `BedAssignment`, `NursingCarePlan`, `MarEntry`, `PatientConsumableUsage`

## 7. Business Rules
| ID | Rule |
|---|---|
| HMS-IPD-BR-001 | Bed cannot be double-occupied. |
| HMS-IPD-BR-002 | MAR administration requires active nursing credential/role. |
| HMS-IPD-BR-003 | Consumable issue decrements inventory via events and charges bill. |

## 8. Approvals
Bed block beyond duration and backdated admission corrections require supervisor approval.

## 9. APIs and Module Ownership
**Owner:** HMS

### APIs
- `POST /api/hms/ipd/admissions`
- `POST /api/hms/ipd/beds/{id}/assign`
- `POST /api/hms/ipd/mar`
- `POST /api/hms/ipd/consumables`

### Events Published
- `PatientAdmitted`
- `BedAssignmentChanged`
- `MarAdministered`
- `ConsumableUsed`

### Events Consumed
- `MedicationDispensed`
- `StockAvailabilityChanged`
- `EmployeeCredentialStatusChanged`

## 10. Notifications
- Bed occupancy alerts
- Overdue MAR alerts

## 11. Reports
- Bed occupancy
- Average length of stay
- MAR compliance

## 12. Audit, Retention, and Privacy
IPD clinical and admin events audited; medication admin records immutable after sign with amendment trail.

## 13. Failure, Idempotency, and Concurrency
- Bed assignment transactional lock
- MAR entry idempotent by doseInstanceId

## 14. Non-Functional Requirements
- Occupancy board near-real-time (<5s)

## 15. Dependencies
- HMS Pharmacy/EMR/Billing
- INV stock
- HRIS credentials
- FIN charges

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HMS-IPD-AC-001 | Admission allocates available bed and starts room rent accrual. |
| HMS-IPD-AC-002 | Administered MAR dose cannot be silently deleted. |
| HMS-IPD-AC-003 | Consumable usage reduces ward store stock. |

## 17. Open Assumptions
- Bed classes map to charge items in billing.

## 18. Source Traceability
Mapped from `§3.1 IPD; §3.2 steps 5` in `Healthcare-ERP-Pathway-and-Workflow.md`.
