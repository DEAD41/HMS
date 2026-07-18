# Financial Reporting & MIS

| Field | Value |
|---|---|
| Module | FIN |
| Sub-module | MIS |
| Status | Draft — pending verification |
| Source | §5.1 Financial reporting & MIS; §9 analytics |

## 1. Scope
P&L, balance sheet, cost-per-patient, department profitability, and management packs from integrated data.

## 2. Exclusions
Board narrative automation AI.

## 3. Actors and Permissions
- CFO
- Controllers
- Department Heads (scoped)

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| FIN-MIS-FR-001 | Generate P&L and balance sheet for periods. |
| FIN-MIS-FR-002 | Compute cost-per-patient and department profitability KPIs. |
| FIN-MIS-FR-003 | Publish management dashboards via FND reporting contracts. |
| FIN-MIS-FR-004 | Support drilldown to journals/source documents per security. |

## 5. Workflow and State Transitions
ReportPack: `Generating -> Ready | Failed`.

## 6. Data / Entities and Validation
- Read models over GL + feeder facts
- KPI definitions cataloged in FND RPT

## 7. Business Rules
| ID | Rule |
|---|---|
| FIN-MIS-BR-001 | Users only see authorized cost centers/facilities. |

## 8. Approvals
Enterprise pack publish may require Controller approval.

## 9. APIs and Module Ownership
**Owner:** FIN

### APIs
- `GET /api/fin/mis/pnl`
- `GET /api/fin/mis/balance-sheet`
- `GET /api/fin/mis/kpis/cost-per-patient`

### Events Published
- `MisPackReady`

### Events Consumed
- `JournalPosted`
- `ReportRunCompleted`

## 10. Notifications
- Pack ready notices

## 11. Reports
- P&L
- Balance sheet
- Cost-per-patient
- Department profitability
- Staff cost ratio (with HRIS facts)

## 12. Audit, Retention, and Privacy
Aggregates preferred; drilldown audited.

## 13. Failure, Idempotency, and Concurrency
- KPI recompute eventual; pin snapshot for published packs

## 14. Non-Functional Requirements
- Interactive financial statements < 3s warmed

## 15. Dependencies
- FIN GL/AR/AP
- HMS/INV/HRIS facts
- FND RPT

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| FIN-MIS-AC-001 | Authorized user can produce department profitability for a month. |
| FIN-MIS-AC-002 | Cost-per-patient KPI available after billing+cost postings. |

## 17. Open Assumptions
- Exact KPI formulas documented in TRACEABILITY/KPI appendix during build.

## 18. Source Traceability
Mapped from `§5.1 Financial reporting & MIS; §9 analytics` in `Healthcare-ERP-Pathway-and-Workflow.md`.
