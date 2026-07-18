# Approval Workflow Engine

| Field | Value |
|---|---|
| Module | FND |
| Sub-module | APPR |
| Status | Draft — pending verification |
| Source | §9 Approval hierarchies; used by HRIS/Procurement/Financials |

## 1. Scope
Configurable approval hierarchies per transaction type and value threshold, reusable across leave/hiring, purchase orders, and payment release.

## 2. Exclusions
Document-centric BPM suite; free-form process designer beyond structured steps.

## 3. Actors and Permissions
- Workflow Admin — define templates
- Approvers — approve/reject/escalate
- Requestors — submit and track

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| FND-APPR-FR-001 | System shall allow defining approval templates by transaction type, facility, and amount/value rules. |
| FND-APPR-FR-002 | Approval routing shall resolve approvers from HRIS org hierarchy and explicit role maps. |
| FND-APPR-FR-003 | Requests shall support approve, reject, request-info, and escalate actions. |
| FND-APPR-FR-004 | Parallel and sequential steps shall be supported. |
| FND-APPR-FR-005 | SLA timers shall escalate overdue approvals. |
| FND-APPR-FR-006 | Modules shall start approvals via a common API and receive decision events. |

## 5. Workflow and State Transitions
```
Draft -> Submitted -> InApproval -> Approved | Rejected | Cancelled
InApproval -> Escalated -> InApproval
```

## 6. Data / Entities and Validation
- `ApprovalTemplate`, `ApprovalStep`, `ApprovalRequest`, `ApprovalAction`
- Value rules: min/max amount, currency, cost center
- Validation: at least one step; no unresolved approver group at runtime start

## 7. Business Rules
| ID | Rule |
|---|---|
| FND-APPR-BR-001 | Requestor cannot approve their own request unless policy explicitly allows. |
| FND-APPR-BR-002 | Rejected requests are immutable except cancellation/archive. |
| FND-APPR-BR-003 | Template changes do not alter in-flight requests. |

## 8. Approvals
Self-governing: template publish may itself require approval for sensitive transaction types.

## 9. APIs and Module Ownership
**Owner:** FND

### APIs
- `POST /api/fnd/approvals/templates`
- `POST /api/fnd/approvals/requests`
- `POST /api/fnd/approvals/requests/{id}/actions`
- `GET /api/fnd/approvals/inbox`

### Events Published
- `ApprovalRequested`
- `ApprovalDecisionMade`
- `ApprovalEscalated`

### Events Consumed
- `EmployeeOrgChanged (HRIS) for routing refresh on new requests`

## 10. Notifications
- Approver inbox notification
- Escalation notification
- Final decision to requestor

## 11. Reports
- Pending approvals aging
- Approval cycle-time by type

## 12. Audit, Retention, and Privacy
Every action immutable with comment, actor, timestamp. Approval artifacts retained with related business transaction retention.

## 13. Failure, Idempotency, and Concurrency
- Action APIs idempotent by actionRequestId.
- Concurrent approve/reject: first commit wins; second gets conflict.
- Missing approver resolution fails request start with clear error.

## 14. Non-Functional Requirements
- Start approval P95 < 300ms.
- Support 10,000 open approval requests.

## 15. Dependencies
- FND IAM
- HRIS org hierarchy
- FND Notifications

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| FND-APPR-AC-001 | PO above threshold routes to correct approver chain. |
| FND-APPR-AC-002 | Overdue step escalates per template SLA. |
| FND-APPR-AC-003 | Decision event is consumed by originating module to advance state. |

## 17. Open Assumptions
- Amount thresholds are in facility base currency unless multi-currency rules configured.
- Delegation/out-of-office can be Phase 2 enhancement if not in MVP.

## 18. Source Traceability
Mapped from `§9 Approval hierarchies; used by HRIS/Procurement/Financials` in `Healthcare-ERP-Pathway-and-Workflow.md`.
