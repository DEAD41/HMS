# Recruitment & Requisitioning

| Field | Value |
|---|---|
| Module | HRIS |
| Sub-module | REC |
| Status | Draft — pending verification |
| Source | §4.1 Recruitment; §4.2 step 1 |

## 1. Scope
Department requisitions, approvals, job posting, screening, interview, and offer.

## 2. Exclusions
External job board product; AI screening marketplace.

## 3. Actors and Permissions
- Department Head
- HR Recruiter
- Interview Panel
- HR Manager

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HRIS-REC-FR-001 | Raise manpower requisition with role, grade, and justification. |
| HRIS-REC-FR-002 | Route requisition through approval hierarchy. |
| HRIS-REC-FR-003 | Manage candidates, interviews, and evaluations. |
| HRIS-REC-FR-004 | Generate offers with compensation components. |
| HRIS-REC-FR-005 | On offer accept, trigger onboarding case. |

## 5. Workflow and State Transitions
Requisition: `Draft -> Submitted -> Approved | Rejected -> Open -> Filled | Cancelled`.
Candidate: `Applied -> Screening -> Interview -> Offered -> Hired | Rejected`.

## 6. Data / Entities and Validation
- `ManpowerRequisition`
- `Candidate`
- `Interview`
- `Offer`

## 7. Business Rules
| ID | Rule |
|---|---|
| HRIS-REC-BR-001 | Cannot hire above approved headcount without exception approval. |
| HRIS-REC-BR-002 | Offer above band requires HR Manager approval. |

## 8. Approvals
Uses FND approval engine with HRIS org hierarchy.

## 9. APIs and Module Ownership
**Owner:** HRIS

### APIs
- `POST /api/hris/requisitions`
- `POST /api/hris/candidates`
- `POST /api/hris/offers`

### Events Published
- `RequisitionApproved`
- `OfferAccepted`

### Events Consumed
- None

## 10. Notifications
- Approver notifications
- Offer expiry reminders

## 11. Reports
- Time-to-hire
- Open requisitions

## 12. Audit, Retention, and Privacy
Candidate PII protected; retention per HR policy.

## 13. Failure, Idempotency, and Concurrency
- Offer accept idempotent
- Concurrent fill of last vacancy: first wins

## 14. Non-Functional Requirements
- Standard CRUD SLAs

## 15. Dependencies
- FND Approvals
- HRIS Employee master

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HRIS-REC-AC-001 | Approved requisition can progress to offer. |
| HRIS-REC-AC-002 | Accepted offer opens onboarding. |

## 17. Open Assumptions
- Job posting channels may be manual initially.

## 18. Source Traceability
Mapped from `§4.1 Recruitment; §4.2 step 1` in `Healthcare-ERP-Pathway-and-Workflow.md`.
