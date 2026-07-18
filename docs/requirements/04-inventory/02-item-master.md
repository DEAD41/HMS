# Item / SKU Master

| Field | Value |
|---|---|
| Module | INV |
| Sub-module | ITEM |
| Status | Draft — pending verification |
| Source | §6.1; §6.2 step 1; §2 item ownership |

## 1. Scope
Register drugs, consumables, implants, and spare parts with UOM, reorder, and batch/expiry rules.

## 2. Exclusions
Global GS1 network management beyond barcode fields.

## 3. Actors and Permissions
- Item Master Steward
- Pharmacist (drug items)
- Biomed Engineer (spares)

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| INV-ITEM-FR-001 | Create/update item master with category, UOM, valuation method, reorder level/safety stock. |
| INV-ITEM-FR-002 | Flag batch/expiry/serial controlled items. |
| INV-ITEM-FR-003 | Publish ItemChanged for HMS/PRC/FIN projections. |
| INV-ITEM-FR-004 | Support item status lifecycle. |

## 5. Workflow and State Transitions
Item: `Draft -> Active -> Suspended -> Obsolete`.

## 6. Data / Entities and Validation
- `Item`
- `ItemUom`
- `ItemReorderPolicy`
- `ItemCategory`

## 7. Business Rules
| ID | Rule |
|---|---|
| INV-ITEM-BR-001 | Active clinical ordering requires active item. |
| INV-ITEM-BR-002 | Valuation method changes restricted when stock exists. |

## 8. Approvals
Valuation method change requires Finance approval.

## 9. APIs and Module Ownership
**Owner:** INV

### APIs
- `POST /api/inv/items`
- `PUT /api/inv/items/{id}`
- `GET /api/inv/items`

### Events Published
- `ItemChanged`

### Events Consumed
- None

## 10. Notifications
- Suspended item used in open orders alerts

## 11. Reports
- Item master extract

## 12. Audit, Retention, and Privacy
Item master changes audited; drug master may include controlled-drug flags.

## 13. Failure, Idempotency, and Concurrency
- Update optimistic concurrency
- Publish outbox with write

## 14. Non-Functional Requirements
- Item search P95 < 300ms

## 15. Dependencies
- FIN valuation accounts mapping
- HMS/PRC consumers

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| INV-ITEM-AC-001 | New drug item available to pharmacy and procurement after activation. |
| INV-ITEM-AC-002 | Suspended item blocked on new POs/orders. |

## 17. Open Assumptions
- Therapeutic classification coding configurable.

## 18. Source Traceability
Mapped from `§6.1; §6.2 step 1; §2 item ownership` in `Healthcare-ERP-Pathway-and-Workflow.md`.
