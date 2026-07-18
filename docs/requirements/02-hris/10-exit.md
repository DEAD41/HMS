# Exit Management

| Field | Value |
|---|---|
| Module | HRIS |
| Sub-module | EXIT |
| Status | Draft — pending verification |
| Source | §4.1 Exit; §4.2 step 7; §4.3 access revoke |

## 1. Scope
Resignation/termination workflow, clearance, full-and-final settlement posting, and access revocation across modules.

## 2. Exclusions
Outplacement services.

## 3. Actors and Permissions
- HR Officer
- Manager
- Finance
- IT/Security

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HRIS-EXIT-FR-001 | Initiate resignation/termination cases. |
| HRIS-EXIT-FR-002 | Run clearance checklist (assets, store returns, clinical handover). |
| HRIS-EXIT-FR-003 | Calculate FnF and post to Financials. |
| HRIS-EXIT-FR-004 | Set employee exited and emit events to disable IAM and clinical scheduling. |
| HRIS-EXIT-FR-005 | Archive employee record. |

## 5. Workflow and State Transitions
ExitCase: `Initiated -> InClearance -> FnFCalculated -> Settled -> Closed`.

## 6. Data / Entities and Validation
- `ExitCase`
- `ClearanceItem`
- `FullAndFinalSettlement`

## 7. Business Rules
| ID | Rule |
|---|---|
| HRIS-EXIT-BR-001 | Exited employees cannot be rostered or authenticate (except legal hold access). |
| HRIS-EXIT-BR-002 | FnF posting idempotent to FIN. |

## 8. Approvals
Termination without notice and FnF exceptions require HR/Finance approvals.

## 9. APIs and Module Ownership
**Owner:** HRIS

### APIs
- `POST /api/hris/exits`
- `POST /api/hris/exits/{id}/clearance`
- `POST /api/hris/exits/{id}/settle`

### Events Published
- `EmployeeExited`
- `FnFPosted`

### Events Consumed
- `ApprovalDecisionMade`

## 10. Notifications
- Clearance pending reminders
- Access revocation confirmation

## 11. Reports
- Exit turnaround
- FnF register

## 12. Audit, Retention, and Privacy
Exit files confidential; retention statutory.

## 13. Failure, Idempotency, and Concurrency
- Settle uses outbox
- Access revoke eventual with retry

## 14. Non-Functional Requirements
- Access revoke propagation < 5 minutes

## 15. Dependencies
- FND IAM
- FIN
- Inventory returns optional

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HRIS-EXIT-AC-001 | Closed exit disables login and removes future roster eligibility. |
| HRIS-EXIT-AC-002 | FnF appears in Financials. |

## 17. Open Assumptions
- Asset return detailed tracking may use Inventory/Assets modules.

## 18. Source Traceability
Mapped from `§4.1 Exit; §4.2 step 7; §4.3 access revoke` in `Healthcare-ERP-Pathway-and-Workflow.md`.
