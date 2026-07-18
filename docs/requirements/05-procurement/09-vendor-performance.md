# Vendor Performance & Compliance Tracking

| Field | Value |
|---|---|
| Module | PRC |
| Sub-module | VPR |
| Status | Draft — pending verification |
| Source | §7.1 performance/compliance; §7.2 step 8 |

## 1. Scope
Track on-time delivery, quality issues, certificate compliance, and ratings used in sourcing.

## 2. Exclusions
External credit rating agencies.

## 3. Actors and Permissions
- Procurement Manager
- QC
- Compliance

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| PRC-VPR-FR-001 | Compute vendor KPIs from GRN timeliness and QC rejections. |
| PRC-VPR-FR-002 | Track regulatory certificate status. |
| PRC-VPR-FR-003 | Maintain vendor scorecards. |
| PRC-VPR-FR-004 | Feed ratings into quote comparison. |
| PRC-VPR-FR-005 | Recommend suspend when KPIs breach thresholds. |

## 5. Workflow and State Transitions
ScorecardPeriod: `Open -> Published`.
Compliance: `Compliant | Warning | NonCompliant`.

## 6. Data / Entities and Validation
- `VendorScorecard`
- `VendorKpiSnapshot`
- certificate status projection

## 7. Business Rules
| ID | Rule |
|---|---|
| PRC-VPR-BR-001 | NonCompliant hard-stop policy can block new awards/POs. |

## 8. Approvals
Suspension recommendation converts to vendor suspend approval.

## 9. APIs and Module Ownership
**Owner:** PRC

### APIs
- `GET /api/prc/vendors/{id}/scorecard`
- `POST /api/prc/vendors/{id}/scorecards/publish`

### Events Published
- `VendorPerformanceUpdated`
- `VendorComplianceChanged`

### Events Consumed
- `GoodsReceived`
- `GoodsRejected`
- `VendorChanged`
- `ApPaymentDisbursed`

## 10. Notifications
- Compliance breach alerts

## 11. Reports
- Vendor scorecards
- Quality rejection trends

## 12. Audit, Retention, and Privacy
Performance records retained for procurement audit.

## 13. Failure, Idempotency, and Concurrency
- KPI recompute idempotent per period

## 14. Non-Functional Requirements
- Scorecard publish batch SLA

## 15. Dependencies
- Vendors
- GRC/QC
- Comparison

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| PRC-VPR-AC-001 | Late delivery reduces on-time KPI. |
| PRC-VPR-AC-002 | Score available in comparison matrix. |

## 17. Open Assumptions
- KPI weights configurable.

## 18. Source Traceability
Mapped from `§7.1 performance/compliance; §7.2 step 8` in `Healthcare-ERP-Pathway-and-Workflow.md`.
