# Quotation Comparison & Selection

| Field | Value |
|---|---|
| Module | PRC |
| Sub-module | CMP |
| Status | Draft — pending verification |
| Source | §7.2 step 4 |

## 1. Scope
Compare quotes on price, lead time, and vendor quality/compliance rating; select award.

## 2. Exclusions
Optimization solver beyond weighted scoring.

## 3. Actors and Permissions
- Buyer
- Procurement Manager
- Evaluation Committee

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| PRC-CMP-FR-001 | Present comparison matrix across quotes. |
| PRC-CMP-FR-002 | Apply scoring weights including vendor performance rating. |
| PRC-CMP-FR-003 | Select winning quote lines and record justification. |
| PRC-CMP-FR-004 | Pass award to PO/contract creation. |

## 5. Workflow and State Transitions
Award: `Recommended -> Approved -> Converted`.

## 6. Data / Entities and Validation
- `QuoteComparison`
- `AwardDecision`

## 7. Business Rules
| ID | Rule |
|---|---|
| PRC-CMP-BR-001 | Cannot award to non-compliant vendor when hard-stop policy on. |
| PRC-CMP-BR-002 | Partial line awards allowed. |

## 8. Approvals
Awards above threshold require approval.

## 9. APIs and Module Ownership
**Owner:** PRC

### APIs
- `POST /api/prc/comparisons`
- `POST /api/prc/comparisons/{id}/award`

### Events Published
- `AwardDecisionMade`

### Events Consumed
- `RfqClosed`
- `VendorPerformanceUpdated`

## 10. Notifications
- Award pending approval

## 11. Reports
- Savings vs estimate
- Award audit

## 12. Audit, Retention, and Privacy
Award justification retained for audit.

## 13. Failure, Idempotency, and Concurrency
- Award idempotent per RFQ line set

## 14. Non-Functional Requirements
- Matrix render interactive

## 15. Dependencies
- RFQ
- Contracts/PO
- Vendor performance

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| PRC-CMP-AC-001 | Award creates basis for PO lines. |
| PRC-CMP-AC-002 | Decision and scores stored. |

## 17. Open Assumptions
- Default weights configurable.

## 18. Source Traceability
Mapped from `§7.2 step 4` in `Healthcare-ERP-Pathway-and-Workflow.md`.
