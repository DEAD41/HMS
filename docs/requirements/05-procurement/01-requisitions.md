# Purchase Requisitions

| Field | Value |
|---|---|
| Module | PRC |
| Sub-module | PR |
| Status | Draft — pending verification |
| Source | §7.1 PR; §7.2 step 1; auto from Store |

## 1. Scope
Manual department requisitions and auto-generated requisitions from Inventory reorder signals.

## 2. Exclusions
Punched-out external punchout catalogs beyond basic.

## 3. Actors and Permissions
- Department Requestor
- Inventory Planner
- Buyer

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| PRC-PR-FR-001 | Create manual PR with items, qty, need-by date, cost center. |
| PRC-PR-FR-002 | Create PR from Inventory PurchaseRequisitionRequested events. |
| PRC-PR-FR-003 | Submit PR into approval flow. |
| PRC-PR-FR-004 | Convert approved PR lines to RFQ or PO. |
| PRC-PR-FR-005 | Prevent duplicate auto-PRs per policy. |

## 5. Workflow and State Transitions
PR: `Draft -> Submitted -> Approved | Rejected -> PartiallyConverted -> Converted | Cancelled`.

## 6. Data / Entities and Validation
- `PurchaseRequisition`
- `PurchaseRequisitionLine`

## 7. Business Rules
| ID | Rule |
|---|---|
| PRC-PR-BR-001 | Auto-PR lines reference item+store+signal id. |
| PRC-PR-BR-002 | Rejected PR not convertible. |

## 8. Approvals
Approval handled in procurement approvals sub-module / FND.

## 9. APIs and Module Ownership
**Owner:** PRC

### APIs
- `POST /api/prc/requisitions`
- `POST /api/prc/requisitions/{id}/submit`
- `POST /api/prc/requisitions/from-signal`

### Events Published
- `PurchaseRequisitionCreated`
- `PurchaseRequisitionApproved`

### Events Consumed
- `PurchaseRequisitionRequested`
- `ApprovalDecisionMade`

## 10. Notifications
- New auto-PR to buyers

## 11. Reports
- PR aging
- Auto vs manual mix

## 12. Audit, Retention, and Privacy
PR audited; department spend visibility.

## 13. Failure, Idempotency, and Concurrency
- from-signal idempotent by signalId
- Submit concurrency safe

## 14. Non-Functional Requirements
- Auto PR creation < 2s after signal consume

## 15. Dependencies
- INV reorder
- FND Approvals
- Items/Vendors

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| PRC-PR-AC-001 | Reorder signal creates a single open PR. |
| PRC-PR-AC-002 | Approved PR can create PO. |

## 17. Open Assumptions
- Consolidation of multiple signals optional.

## 18. Source Traceability
Mapped from `§7.1 PR; §7.2 step 1; auto from Store` in `Healthcare-ERP-Pathway-and-Workflow.md`.
