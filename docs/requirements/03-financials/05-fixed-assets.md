# Fixed Assets & Biomedical Depreciation

| Field | Value |
|---|---|
| Module | FIN |
| Sub-module | FA |
| Status | Draft — pending verification |
| Source | §5.1 Fixed Assets; equipment from Procurement; spares linkage |

## 1. Scope
Asset register for equipment, capitalization from procurement, depreciation schedules, and maintenance cost linkage.

## 2. Exclusions
Full CMMS replacement; IoT telemetry.

## 3. Actors and Permissions
- Asset Accountant
- Biomedical Engineer
- Finance Controller

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| FIN-FA-FR-001 | Create assets from capitalized PO/GRN or manual entry. |
| FIN-FA-FR-002 | Maintain depreciation methods and run periodic depreciation. |
| FIN-FA-FR-003 | Record transfers, disposal, and impairment. |
| FIN-FA-FR-004 | Attach maintenance cost from spare issues. |
| FIN-FA-FR-005 | Provide asset register reports. |

## 5. Workflow and State Transitions
Asset: `Draft -> Active -> UnderMaintenance -> Disposed | FullyDepreciated`.
DepreciationRun: `Draft -> Posted`.

## 6. Data / Entities and Validation
- `FixedAsset`
- `DepreciationSchedule`
- `DepreciationRun`
- `AssetMaintenanceCost`

## 7. Business Rules
| ID | Rule |
|---|---|
| FIN-FA-BR-001 | Disposed assets stop depreciation. |
| FIN-FA-BR-002 | Capitalization thresholds configurable. |

## 8. Approvals
Disposal and impairment require approval.

## 9. APIs and Module Ownership
**Owner:** FIN

### APIs
- `POST /api/fin/assets`
- `POST /api/fin/assets/depreciation-runs`
- `POST /api/fin/assets/{id}/dispose`

### Events Published
- `AssetCreated`
- `DepreciationPosted`
- `AssetDisposed`

### Events Consumed
- `GoodsReceived (capital)`
- `SparePartIssued`

## 10. Notifications
- Depreciation due reminders

## 11. Reports
- Asset register
- Depreciation forecast

## 12. Audit, Retention, and Privacy
Asset history retained for audit/regulatory device tracking as applicable.

## 13. Failure, Idempotency, and Concurrency
- Depreciation posting idempotent per period/asset

## 14. Non-Functional Requirements
- Monthly depreciation batch SLA configurable

## 15. Dependencies
- PRC/INV
- FIN GL

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| FIN-FA-AC-001 | Capital equipment GRN can create asset. |
| FIN-FA-AC-002 | Spare issue adds maintenance cost to asset. |

## 17. Open Assumptions
- Componentization optional later.

## 18. Source Traceability
Mapped from `§5.1 Fixed Assets; equipment from Procurement; spares linkage` in `Healthcare-ERP-Pathway-and-Workflow.md`.
