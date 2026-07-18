# Equipment Breakdown to Spares & Depreciation Impact

| Field | Value |
|---|---|
| Module | XWF |
| Sub-module | EQM |
| Status | Draft — pending verification |
| Source | §8 equipment loop; §6.3; §5.3 assets |

## 1. Scope
Link biomedical fault logging to spare issue and asset maintenance cost / depreciation context.

## 2. Exclusions
Full CMMS may own fault tickets later; MVP accepts maintenance event with asset id.

## 3. Actors and Permissions
- Biomed
- Store
- Asset Accountant

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| XWF-EQM-FR-001 | Capture maintenance need against asset id (HMS biomed log or FIN asset service). |
| XWF-EQM-FR-002 | Issue spare from Inventory against asset. |
| XWF-EQM-FR-003 | Financials adds maintenance cost to asset. |
| XWF-EQM-FR-004 | Depreciation continues unless disposal/impairment workflow says otherwise. |

## 5. Workflow and State Transitions
FaultLogged -> SpareIssued -> AssetMaintenanceCostUpdated -> (optional) Impairment/Disposal.

## 6. Data / Entities and Validation
- assetId
- spareIssueId

## 7. Business Rules
| ID | Rule |
|---|---|
| XWF-EQM-BR-001 | Spare-classified items require asset id. |
| XWF-EQM-BR-002 | Costs not double-posted on event retry. |

## 8. Approvals
Impairment/disposal approvals in FIN FA.

## 9. APIs and Module Ownership
**Owner:** XWF

### APIs
- `Existing APIs`

### Events Published
- `SparePartIssued`
- `AssetMaintenanceCostUpdated`

### Events Consumed
- `AssetCreated`

## 10. Notifications
- Critical equipment down alerts (if logged)

## 11. Reports
- Maintenance cost by asset

## 12. Audit, Retention, and Privacy
Device history retained.

## 13. Failure, Idempotency, and Concurrency
- Idempotent cost append by spareIssueId

## 14. Non-Functional Requirements
- Event hop < 5s

## 15. Dependencies
- INV SPR
- FIN FA

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| XWF-EQM-AC-001 | Spare issue increases asset maintenance cost once. |
| XWF-EQM-AC-002 | Stock decremented. |

## 17. Open Assumptions
- Standalone CMMS integration later.

## 18. Source Traceability
Mapped from `§8 equipment loop; §6.3; §5.3 assets` in `Healthcare-ERP-Pathway-and-Workflow.md`.
