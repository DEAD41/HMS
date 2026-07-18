# Central Store / Sub-stores / Bins

| Field | Value |
|---|---|
| Module | INV |
| Sub-module | STR |
| Status | Draft — pending verification |
| Source | §6.1 stores; warehouse/bin |

## 1. Scope
Configure central store, pharmacy/ward/OT stores, and bin locations.

## 2. Exclusions
Automated warehouse robotics.

## 3. Actors and Permissions
- Store Admin
- Store Keeper

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| INV-STR-FR-001 | Create stores linked to facilities/org units. |
| INV-STR-FR-002 | Configure bins/locations within stores. |
| INV-STR-FR-003 | Define which stores serve which clinical units. |
| INV-STR-FR-004 | Activate/deactivate stores with stock constraints. |

## 5. Workflow and State Transitions
Store: `Draft -> Active -> Inactive`.

## 6. Data / Entities and Validation
- `Store`
- `Bin`
- `StoreServiceArea`

## 7. Business Rules
| ID | Rule |
|---|---|
| INV-STR-BR-001 | Cannot inactivate store with non-zero stock without transfer/write-off. |
| INV-STR-BR-002 | Pharmacy stores must support batch tracking. |

## 8. Approvals
Store inactivation requires approval if stock remains.

## 9. APIs and Module Ownership
**Owner:** INV

### APIs
- `POST /api/inv/stores`
- `POST /api/inv/bins`

### Events Published
- `StoreChanged`

### Events Consumed
- None

## 10. Notifications
- Inactive store with stock alerts

## 11. Reports
- Store list with valuations summary

## 12. Audit, Retention, and Privacy
Configuration changes audited.

## 13. Failure, Idempotency, and Concurrency
- Optimistic concurrency

## 14. Non-Functional Requirements
- Standard SLAs

## 15. Dependencies
- FND Tenancy

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| INV-STR-AC-001 | Active pharmacy store selectable for dispense allocation. |

## 17. Open Assumptions
- Default bin optional per store.

## 18. Source Traceability
Mapped from `§6.1 stores; warehouse/bin` in `Healthcare-ERP-Pathway-and-Workflow.md`.
