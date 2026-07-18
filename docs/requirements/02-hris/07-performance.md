# Performance Management & Appraisals

| Field | Value |
|---|---|
| Module | HRIS |
| Sub-module | PRF |
| Status | Draft — pending verification |
| Source | §4.1 Performance; §4.2 step 6 |

## 1. Scope
Periodic appraisals, goals, and ratings that may inform privileges/training plans.

## 2. Exclusions
Full OKR enterprise suite.

## 3. Actors and Permissions
- Employee
- Manager
- HR BP

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HRIS-PRF-FR-001 | Define appraisal cycles and templates. |
| HRIS-PRF-FR-002 | Capture self/manager reviews and ratings. |
| HRIS-PRF-FR-003 | Finalize appraisal outcomes. |
| HRIS-PRF-FR-004 | Link development actions to training module. |

## 5. Workflow and State Transitions
Appraisal: `NotStarted -> SelfReview -> ManagerReview -> Calibration -> Finalized`.

## 6. Data / Entities and Validation
- `AppraisalCycle`
- `AppraisalForm`
- `Rating`

## 7. Business Rules
| ID | Rule |
|---|---|
| HRIS-PRF-BR-001 | Finalized appraisals immutable except formal appeal process. |

## 8. Approvals
Calibration changes may require HR approval.

## 9. APIs and Module Ownership
**Owner:** HRIS

### APIs
- `POST /api/hris/appraisals`
- `POST /api/hris/appraisals/{id}/finalize`

### Events Published
- `AppraisalFinalized`

### Events Consumed
- None

## 10. Notifications
- Cycle deadline reminders

## 11. Reports
- Rating distribution

## 12. Audit, Retention, and Privacy
Performance data confidential.

## 13. Failure, Idempotency, and Concurrency
- Finalize idempotent

## 14. Non-Functional Requirements
- Standard SLAs

## 15. Dependencies
- HRIS Employee
- Training

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HRIS-PRF-AC-001 | Finalized appraisal stored and visible to authorized parties. |

## 17. Open Assumptions
- Compensation linkage optional later.

## 18. Source Traceability
Mapped from `§4.1 Performance; §4.2 step 6` in `Healthcare-ERP-Pathway-and-Workflow.md`.
