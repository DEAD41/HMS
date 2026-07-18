# Training / CME Tracking

| Field | Value |
|---|---|
| Module | HRIS |
| Sub-module | TRN |
| Status | Draft — pending verification |
| Source | §4.1 Training/CME; §4.2 step 6 |

## 1. Scope
Track CME/training completions and certification renewals feeding credentialing alerts.

## 2. Exclusions
Full e-learning content delivery platform.

## 3. Actors and Permissions
- Training Coordinator
- Clinician
- Credentialing Officer

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HRIS-TRN-FR-001 | Catalog training/CME activities. |
| HRIS-TRN-FR-002 | Record attendance/completion and credit hours. |
| HRIS-TRN-FR-003 | Link completions to credential renewals. |
| HRIS-TRN-FR-004 | Alert on missing mandatory training. |

## 5. Workflow and State Transitions
TrainingAssignment: `Assigned -> InProgress -> Completed | Overdue`.

## 6. Data / Entities and Validation
- `TrainingCourse`
- `TrainingAssignment`
- `CmeCredit`

## 7. Business Rules
| ID | Rule |
|---|---|
| HRIS-TRN-BR-001 | Mandatory training overdue can suspend selected privileges per policy. |

## 8. Approvals
Policy exceptions approved by Medical Director/HR.

## 9. APIs and Module Ownership
**Owner:** HRIS

### APIs
- `POST /api/hris/training/assignments`
- `POST /api/hris/training/completions`

### Events Published
- `TrainingCompleted`
- `MandatoryTrainingOverdue`

### Events Consumed
- `CredentialExpiring`

## 10. Notifications
- Overdue mandatory training alerts

## 11. Reports
- CME hours by clinician
- Compliance rate

## 12. Audit, Retention, and Privacy
Training records retained with credential evidence.

## 13. Failure, Idempotency, and Concurrency
- Completion posting idempotent

## 14. Non-Functional Requirements
- Standard SLAs

## 15. Dependencies
- Credentialing
- Notifications

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HRIS-TRN-AC-001 | Completion updates CME credits and can clear renewal prerequisites. |

## 17. Open Assumptions
- External CME providers via manual credit entry initially.

## 18. Source Traceability
Mapped from `§4.1 Training/CME; §4.2 step 6` in `Healthcare-ERP-Pathway-and-Workflow.md`.
