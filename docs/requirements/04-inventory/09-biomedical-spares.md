# Biomedical Equipment Spares

| Field | Value |
|---|---|
| Module | INV |
| Sub-module | SPR |
| Status | Draft — pending verification |
| Source | §6.1 biomedical spares; §6.3 asset linkage; §8 equipment loop |

## 1. Scope
Manage spare parts inventory for biomedical equipment and link usage to asset maintenance records in Financials.

## 2. Exclusions
Full CMMS work-order suite (can integrate later).

## 3. Actors and Permissions
- Biomed Engineer
- Store Keeper
- Asset Accountant

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| INV-SPR-FR-001 | Classify items as spares linked to asset categories/models. |
| INV-SPR-FR-002 | Issue spares against equipment/asset id. |
| INV-SPR-FR-003 | Record maintenance usage notes. |
| INV-SPR-FR-004 | Emit events to update asset maintenance cost. |

## 5. Workflow and State Transitions
SpareIssue extends stock issue with `assetId` required.

## 6. Data / Entities and Validation
- `SpareItemProfile`
- `SpareIssue` (specialization of issue)

## 7. Business Rules
| ID | Rule |
|---|---|
| INV-SPR-BR-001 | Spare issue without asset id blocked for spare-classified items. |
| INV-SPR-BR-002 | Costs post to asset maintenance + cost center. |

## 8. Approvals
Cannibalization/high-value spare issues may require approval.

## 9. APIs and Module Ownership
**Owner:** INV

### APIs
- `POST /api/inv/spares/issues`
- `GET /api/inv/spares/by-asset/{assetId}`

### Events Published
- `SparePartIssued`

### Events Consumed
- `AssetCreated`
- `ItemChanged`

## 10. Notifications
- Critical spare stock-out alerts

## 11. Reports
- Spares consumption by asset
- MTTR support extracts

## 12. Audit, Retention, and Privacy
Device maintenance history linkage retained.

## 13. Failure, Idempotency, and Concurrency
- Issue idempotent
- Asset ref validated against FIN projection

## 14. Non-Functional Requirements
- Standard SLAs

## 15. Dependencies
- FIN Fixed Assets
- Issues

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| INV-SPR-AC-001 | Spare issue increments asset maintenance cost in Financials. |
| INV-SPR-AC-002 | Stock decremented. |

## 17. Open Assumptions
- Work order module may be added later; assetId sufficient for MVP.

## 18. Source Traceability
Mapped from `§6.1 biomedical spares; §6.3 asset linkage; §8 equipment loop` in `Healthcare-ERP-Pathway-and-Workflow.md`.
