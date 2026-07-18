# Reporting & Analytics Contracts

| Field | Value |
|---|---|
| Module | FND |
| Sub-module | RPT |
| Status | Draft — pending verification |
| Source | §9 Reporting & analytics; cost-per-patient, profitability, turnover, staff cost, vendor performance |

## 1. Scope
Unified MIS/BI layer contracts and operational report APIs pulling from all modules without breaking ownership boundaries.

## 2. Exclusions
Full custom pixel-perfect report designer in Phase 1; advanced AI analytics in Phase 4.

## 3. Actors and Permissions
- Executives / Department heads — consume dashboards
- Report Admin — publish report definitions
- Modules — provide read models / export facts

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| FND-RPT-FR-001 | Each module shall publish analytical fact/projection contracts for approved metrics. |
| FND-RPT-FR-002 | Foundation shall provide a report catalog and parameterized execution API. |
| FND-RPT-FR-003 | Dashboards shall enforce the same RBAC and facility scoping as operational data. |
| FND-RPT-FR-004 | Standard KPI set shall include cost-per-patient, department profitability, inventory turnover, staff cost ratio, and vendor performance. |
| FND-RPT-FR-005 | Exports shall be auditable. |

## 5. Workflow and State Transitions
ReportDefinition: `Draft -> Published -> Retired`.
ReportRun: `Queued -> Running -> Succeeded | Failed`.

## 6. Data / Entities and Validation
- `ReportDefinition`, `ReportRun`, semantic KPI identifiers
- Fact tables/projections owned per module, cataloged centrally

## 7. Business Rules
| ID | Rule |
|---|---|
| FND-RPT-BR-001 | Reports cannot bypass row-level facility security. |
| FND-RPT-BR-002 | Heavy reports run asynchronously. |

## 8. Approvals
Publishing enterprise-wide financial reports may require Finance Controller approval.

## 9. APIs and Module Ownership
**Owner:** FND

### APIs
- `GET /api/fnd/reports`
- `POST /api/fnd/reports/{key}/runs`
- `GET /api/fnd/reports/runs/{id}`
- `GET /api/fnd/kpis/{key}`

### Events Published
- `ReportRunCompleted`

### Events Consumed
- `Module fact projection updates`

## 10. Notifications
- Report completion notice

## 11. Reports
- All catalog reports listed in module files

## 12. Audit, Retention, and Privacy
Report access and exports audited. Aggregates preferred over row-level PHI.

## 13. Failure, Idempotency, and Concurrency
- Report runs idempotent by runRequestId.
- Timeouts mark Failed with retry option.

## 14. Non-Functional Requirements
- Interactive KPI cards P95 < 2s on warmed aggregates.
- Async large export within configured SLA.

## 15. Dependencies
- All modules' reporting projections
- FND IAM

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| FND-RPT-AC-001 | Authorized user can run department profitability for their facility. |
| FND-RPT-AC-002 | Unauthorized cross-facility report is denied. |

## 17. Open Assumptions
- Initial implementation may use SQL views/read models; OLAP warehouse optional later.

## 18. Source Traceability
Mapped from `§9 Reporting & analytics; cost-per-patient, profitability, turnover, staff cost, vendor performance` in `Healthcare-ERP-Pathway-and-Workflow.md`.
