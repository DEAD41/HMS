# Contract & Rate-Contract Management

| Field | Value |
|---|---|
| Module | PRC |
| Sub-module | CTR |
| Status | Draft — pending verification |
| Source | §7.1 contracts; §7.2 step 3 rate contract path |

## 1. Scope
Manage contracts/rate contracts especially for pharma and high-volume consumables.

## 2. Exclusions
Complex CLM clause AI negotiation.

## 3. Actors and Permissions
- Contract Manager
- Buyer
- Legal/Compliance

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| PRC-CTR-FR-001 | Create rate contracts with items, prices, validity, and volume commitments. |
| PRC-CTR-FR-002 | Release POs against contracts without RFQ when valid. |
| PRC-CTR-FR-003 | Track call-off quantities and expiry. |
| PRC-CTR-FR-004 | Manage amendments. |

## 5. Workflow and State Transitions
Contract: `Draft -> InApproval -> Active -> Expired | Terminated`.

## 6. Data / Entities and Validation
- `PurchaseContract`
- `ContractLine`
- `ContractAmendment`

## 7. Business Rules
| ID | Rule |
|---|---|
| PRC-CTR-BR-001 | Expired contracts cannot release new POs. |
| PRC-CTR-BR-002 | Price on call-off taken from contract unless amendment. |

## 8. Approvals
Contract activation uses approval workflow.

## 9. APIs and Module Ownership
**Owner:** PRC

### APIs
- `POST /api/prc/contracts`
- `POST /api/prc/contracts/{id}/activate`
- `POST /api/prc/contracts/{id}/call-off`

### Events Published
- `ContractActivated`
- `ContractExpired`

### Events Consumed
- `ApprovalDecisionMade`
- `ItemChanged`
- `VendorChanged`

## 10. Notifications
- Contract expiry alerts

## 11. Reports
- Contract utilization
- Price variance vs spot

## 12. Audit, Retention, and Privacy
Contracts retained for commercial/statutory periods.

## 13. Failure, Idempotency, and Concurrency
- Call-off concurrency controls on remaining qty

## 14. Non-Functional Requirements
- Standard SLAs

## 15. Dependencies
- Vendors/Items
- PO
- Approvals

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| PRC-CTR-AC-001 | Active rate contract can generate PO without RFQ. |
| PRC-CTR-AC-002 | Expiry prevents further call-off. |

## 17. Open Assumptions
- Legal e-sign optional.

## 18. Source Traceability
Mapped from `§7.1 contracts; §7.2 step 3 rate contract path` in `Healthcare-ERP-Pathway-and-Workflow.md`.
