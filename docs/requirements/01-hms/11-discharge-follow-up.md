# Discharge & Follow-up

| Field | Value |
|---|---|
| Module | HMS |
| Sub-module | DIS |
| Status | Draft — pending verification |
| Source | §3.1 Discharge; §3.2 steps 8–9 |

## 1. Scope
Discharge reconciliation, discharge summary, follow-up appointment creation, prescription handoff, and post-discharge claim tracking handoff.

## 2. Exclusions
Full remote patient monitoring.

## 3. Actors and Permissions
- Attending Physician
- Ward Nurse
- Billing Officer
- Medical Records

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HMS-DIS-FR-001 | Initiate discharge with clinical criteria checklist. |
| HMS-DIS-FR-002 | Reconcile final bill before discharge completion (policy-configurable). |
| HMS-DIS-FR-003 | Generate discharge summary and instructions. |
| HMS-DIS-FR-004 | Create follow-up appointment and hand off outpatient prescription. |
| HMS-DIS-FR-005 | Trigger insurance outstanding tracking in Financials. |
| HMS-DIS-FR-006 | Release bed on discharge completion. |

## 5. Workflow and State Transitions
Discharge: `Initiated -> ClinicalClearance -> BillingClearance -> Completed | Cancelled`.

## 6. Data / Entities and Validation
- `DischargeProcess`
- `DischargeSummary`
- follow-up appointment link
- prescription handoff

## 7. Business Rules
| ID | Rule |
|---|---|
| HMS-DIS-BR-001 | Cannot complete discharge with incomplete mandatory summary sections. |
| HMS-DIS-BR-002 | Open critical results may warn/block per policy. |
| HMS-DIS-BR-003 | Bed release only after completion. |

## 8. Approvals
Discharge against unpaid self-pay balance may require waiver approval.

## 9. APIs and Module Ownership
**Owner:** HMS

### APIs
- `POST /api/hms/discharge`
- `POST /api/hms/discharge/{id}/summary`
- `POST /api/hms/discharge/{id}/complete`

### Events Published
- `DischargeCompleted`
- `FollowUpScheduled`
- `ClaimSubmissionRequested`

### Events Consumed
- `InvoiceFinalized`
- `PaymentReceived`

## 10. Notifications
- Pending clearance alerts

## 11. Reports
- Discharge volume
- Discharge delay reasons

## 12. Audit, Retention, and Privacy
Discharge summaries are legal medical records; retention with clinical record policy.

## 13. Failure, Idempotency, and Concurrency
- Complete discharge saga compensates on failure (no silent bed leak)

## 14. Non-Functional Requirements
- Discharge complete under 3s excluding user input

## 15. Dependencies
- HMS IPD/Billing/Pharmacy/EMR
- FIN AR claims

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HMS-DIS-AC-001 | Completed discharge frees bed and finalizes clinical summary. |
| HMS-DIS-AC-002 | Follow-up appointment visible in front office schedule. |
| HMS-DIS-AC-003 | Outstanding insurance portion tracked in AR. |

## 17. Open Assumptions
- Patient portal visibility Phase 4.

## 18. Source Traceability
Mapped from `§3.1 Discharge; §3.2 steps 8–9` in `Healthcare-ERP-Pathway-and-Workflow.md`.
