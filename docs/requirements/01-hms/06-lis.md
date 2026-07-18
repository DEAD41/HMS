# Laboratory Information System (LIS)

| Field | Value |
|---|---|
| Module | HMS |
| Sub-module | LIS |
| Status | Draft — pending verification |
| Source | §3.1 LIS; §3.2 order fulfillment labs |

## 1. Scope
Lab order intake, sample collection, processing, result entry/validation, and auto-post to EMR.

## 2. Exclusions
Full analyzer middleware device drivers beyond generic interface adapter; external reference lab network portal.

## 3. Actors and Permissions
- Phlebotomist
- Lab Technologist
- Pathologist
- Ordering Clinician (read)

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HMS-LIS-FR-001 | Receive clinical lab orders from EMR/OPD/IPD/ER. |
| HMS-LIS-FR-002 | Generate sample collection lists and capture sample IDs. |
| HMS-LIS-FR-003 | Track sample lifecycle and rejects/recollects. |
| HMS-LIS-FR-004 | Enter/import results and support clinical validation/sign-out. |
| HMS-LIS-FR-005 | Auto-post finalized results to EMR and notify ordering clinician. |
| HMS-LIS-FR-006 | Post diagnostic charges on order accept/complete per billing rules. |

## 5. Workflow and State Transitions
Order: `Received -> Collected -> InProcess -> Preliminary -> Final | Cancelled`.
Sample: `Collected -> Accepted | Rejected`.

## 6. Data / Entities and Validation
- `LabOrder`
- `LabSample`
- `LabResult`
- `Analyte` master refs

## 7. Business Rules
| ID | Rule |
|---|---|
| HMS-LIS-BR-001 | Final result requires authorized validator role. |
| HMS-LIS-BR-002 | Critical values trigger mandatory notification. |
| HMS-LIS-BR-003 | Amended results create new version linked to prior final. |

## 8. Approvals
Manual charge write-off for cancelled lab after resulting requires billing approval.

## 9. APIs and Module Ownership
**Owner:** HMS

### APIs
- `POST /api/hms/lis/orders/accept`
- `POST /api/hms/lis/samples`
- `POST /api/hms/lis/results`
- `POST /api/hms/lis/results/{id}/finalize`

### Events Published
- `LabOrderAccepted`
- `LabResultPosted`
- `CriticalValueAlert`

### Events Consumed
- `ClinicalOrderPlaced`

## 10. Notifications
- Critical value alerts
- Recollect requests

## 11. Reports
- TAT by test
- Critical value log
- Workload

## 12. Audit, Retention, and Privacy
Lab results are clinical records; amendments audited; retention per lab regulations.

## 13. Failure, Idempotency, and Concurrency
- Result finalize idempotent
- Sample ID unique per facility

## 14. Non-Functional Requirements
- Result post to EMR lag P95 < 5s

## 15. Dependencies
- HMS EMR/Billing
- FND Notifications

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HMS-LIS-AC-001 | Finalized result appears in patient EMR. |
| HMS-LIS-AC-002 | Critical result notifies ordering clinician. |

## 17. Open Assumptions
- Device integration adapters phased after core LIS.

## 18. Source Traceability
Mapped from `§3.1 LIS; §3.2 order fulfillment labs` in `Healthcare-ERP-Pathway-and-Workflow.md`.
