# Reorder Planning & Auto Requisition

| Field | Value |
|---|---|
| Module | INV |
| Sub-module | ROP |
| Status | Draft — pending verification |
| Source | §6.1 min/max/reorder; §6.2 step 4; §6.3 auto PR |

## 1. Scope
Monitor min/max/reorder points and auto-create purchase requisitions in Procurement.

## 2. Exclusions
Advanced forecasting ML.

## 3. Actors and Permissions
- Inventory Planner
- Store Supervisor
- Procurement (consumer)

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| INV-ROP-FR-001 | Maintain reorder parameters per item/store. |
| INV-ROP-FR-002 | Evaluate net availability against reorder point continuously/on events. |
| INV-ROP-FR-003 | Auto-create purchase requisitions with suggested qty. |
| INV-ROP-FR-004 | Avoid duplicate open requisitions for same item/store per policy. |
| INV-ROP-FR-005 | Support manual planned requisitions. |

## 5. Workflow and State Transitions
ReorderSignal: `Detected -> RequisitionCreated -> Suppressed`.
Suppressed when open PR/PO covers demand.

## 6. Data / Entities and Validation
- `ReorderPolicy`
- `ReorderSignal`
- link to PRC requisition id

## 7. Business Rules
| ID | Rule |
|---|---|
| INV-ROP-BR-001 | Auto-PR only for active items/vendors category rules. |
| INV-ROP-BR-002 | Signal deduped while covering docs open. |

## 8. Approvals
Auto-PR above value may still need procurement approval later.

## 9. APIs and Module Ownership
**Owner:** INV

### APIs
- `POST /api/inv/reorder-policies`
- `POST /api/inv/reorder/evaluate`
- `GET /api/inv/reorder/signals`

### Events Published
- `ReorderPointBreached`
- `PurchaseRequisitionRequested`

### Events Consumed
- `StockIssued`
- `StockIncreased`
- `ItemChanged`

## 10. Notifications
- Reorder breach alerts

## 11. Reports
- Items below reorder
- Auto-PR hit rate

## 12. Audit, Retention, and Privacy
Planning actions audited.

## 13. Failure, Idempotency, and Concurrency
- Evaluate idempotent per item/store snapshot
- Outbox to PRC

## 14. Non-Functional Requirements
- Evaluate on event path < 500ms

## 15. Dependencies
- PRC requisitions
- Issues/Receipts

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| INV-ROP-AC-001 | Dispense that crosses reorder creates PR request event consumed by Procurement. |
| INV-ROP-AC-002 | No duplicate PR while one open. |

## 17. Open Assumptions
- Safety stock formulas simple min/max initially.

## 18. Source Traceability
Mapped from `§6.1 min/max/reorder; §6.2 step 4; §6.3 auto PR` in `Healthcare-ERP-Pathway-and-Workflow.md`.
