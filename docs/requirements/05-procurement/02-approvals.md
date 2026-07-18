# Procurement Approval Routing

| Field | Value |
|---|---|
| Module | PRC |
| Sub-module | PAP |
| Status | Draft — pending verification |
| Source | §7.2 step 2; HRIS org hierarchy |

## 1. Scope
Value-based purchase approval routing using HRIS organizational hierarchy and FND approval engine.

## 2. Exclusions
Separate from FND engine implementation—this specifies procurement policies.

## 3. Actors and Permissions
- Buyer
- Department Head
- Finance Controllers
- CFO (high value)

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| PRC-PAP-FR-001 | Map PR/PO/contract transaction types to approval templates by value bands. |
| PRC-PAP-FR-002 | Resolve approvers from HRIS reporting lines and role maps. |
| PRC-PAP-FR-003 | Block conversion/issue until approved. |
| PRC-PAP-FR-004 | Record decision trail on procurement documents. |

## 5. Workflow and State Transitions
Uses FND approval states attached to PR/PO/Contract.

## 6. Data / Entities and Validation
- Policy config entities linking thresholds to templates

## 7. Business Rules
| ID | Rule |
|---|---|
| PRC-PAP-BR-001 | Requestor cannot self-approve unless policy allows. |
| PRC-PAP-BR-002 | Policy changes do not rewrite in-flight approvals. |

## 8. Approvals
Managed via FND Approvals; procurement owns threshold policies.

## 9. APIs and Module Ownership
**Owner:** PRC

### APIs
- `PUT /api/prc/approval-policies`
- `POST /api/prc/{docType}/{id}/send-for-approval`

### Events Published
- `ProcurementApprovalRequested`

### Events Consumed
- `ApprovalDecisionMade`
- `EmployeeOrgChanged`

## 10. Notifications
- Approver inbox via FND

## 11. Reports
- Approval cycle time by value band

## 12. Audit, Retention, and Privacy
Approval decisions retained with commercial documents.

## 13. Failure, Idempotency, and Concurrency
- Send-for-approval idempotent

## 14. Non-Functional Requirements
- Start approval < 300ms

## 15. Dependencies
- FND APPR
- HRIS org
- PR/PO/Contracts

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| PRC-PAP-AC-001 | PO above threshold cannot issue without approvals complete. |

## 17. Open Assumptions
- Delegation covered by FND capability roadmap.

## 18. Source Traceability
Mapped from `§7.2 step 2; HRIS org hierarchy` in `Healthcare-ERP-Pathway-and-Workflow.md`.
