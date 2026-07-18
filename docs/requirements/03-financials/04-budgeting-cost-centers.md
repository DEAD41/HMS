# Budgeting & Cost-Center Control

| Field | Value |
|---|---|
| Module | FIN |
| Sub-module | BUD |
| Status | Draft — pending verification |
| Source | §5.1 Budgeting; §5.2 D |

## 1. Scope
Annual/quarterly budgets per cost center and real-time variance against procurement, store issues, and payroll.

## 2. Exclusions
Driver-based predictive budgeting AI.

## 3. Actors and Permissions
- Department Head
- Finance Controller
- Budget Analyst

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| FIN-BUD-FR-001 | Maintain cost centers and hierarchies. |
| FIN-BUD-FR-002 | Capture budgets by period/account/cost center. |
| FIN-BUD-FR-003 | Track actuals from postings/events. |
| FIN-BUD-FR-004 | Raise variance alerts when thresholds breached. |
| FIN-BUD-FR-005 | Optionally hard-stop or warn procurement commitments over budget. |

## 5. Workflow and State Transitions
BudgetVersion: `Draft -> Submitted -> Approved -> Active -> Closed`.

## 6. Data / Entities and Validation
- `CostCenter`
- `BudgetVersion`
- `BudgetLine`
- `VarianceAlert`

## 7. Business Rules
| ID | Rule |
|---|---|
| FIN-BUD-BR-001 | Active budget required for hard-control mode. |
| FIN-BUD-BR-002 | Actuals are derived, not manually overriding posted facts. |

## 8. Approvals
Budget approval via FND engine.

## 9. APIs and Module Ownership
**Owner:** FIN

### APIs
- `POST /api/fin/cost-centers`
- `POST /api/fin/budgets`
- `GET /api/fin/budgets/variance`

### Events Published
- `CostCenterChanged`
- `BudgetApproved`
- `BudgetVarianceBreached`

### Events Consumed
- `JournalPosted`
- `PurchaseOrderIssued`
- `StockIssued`
- `PayrollPosted`

## 10. Notifications
- Variance alerts to dept heads/controllers

## 11. Reports
- Budget vs actual
- Department burn rate

## 12. Audit, Retention, and Privacy
Budget artifacts retained with financial planning records.

## 13. Failure, Idempotency, and Concurrency
- Variance calc eventual consistent with posting lag tolerance

## 14. Non-Functional Requirements
- Variance dashboard < 3s

## 15. Dependencies
- FIN GL
- PRC
- INV
- HRIS payroll
- FND Notifications

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| FIN-BUD-AC-001 | Approved budget visible for control checks. |
| FIN-BUD-AC-002 | Over-threshold PO triggers warn/block per config. |

## 17. Open Assumptions
- Hard control optional per facility.

## 18. Source Traceability
Mapped from `§5.1 Budgeting; §5.2 D` in `Healthcare-ERP-Pathway-and-Workflow.md`.
