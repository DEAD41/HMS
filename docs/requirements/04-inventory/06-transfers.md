# Inter-store Transfers

| Field | Value |
|---|---|
| Module | INV |
| Sub-module | XFER |
| Status | Draft — pending verification |
| Source | §6.1 transfers; §6.2 step 7 |

## 1. Scope
Transfer stock between stores with full audit trail.

## 2. Exclusions
Cross-facility logistics optimization beyond simple transfer docs.

## 3. Actors and Permissions
- Store Keeper
- Store Supervisor

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| INV-XFER-FR-001 | Create transfer orders between stores. |
| INV-XFER-FR-002 | Ship and receive transfer quantities/batches. |
| INV-XFER-FR-003 | Handle in-transit and variances. |
| INV-XFER-FR-004 | Maintain audit trail. |

## 5. Workflow and State Transitions
Transfer: `Draft -> InTransit -> Received | Cancelled`.
Variance investigation sub-state when qty mismatch.

## 6. Data / Entities and Validation
- `StockTransfer`
- `StockTransferLine`

## 7. Business Rules
| ID | Rule |
|---|---|
| INV-XFER-BR-001 | In-transit stock not issuable from either store. |
| INV-XFER-BR-002 | Partial receipts allowed. |

## 8. Approvals
Variance write-off/adjustment requires approval.

## 9. APIs and Module Ownership
**Owner:** INV

### APIs
- `POST /api/inv/transfers`
- `POST /api/inv/transfers/{id}/ship`
- `POST /api/inv/transfers/{id}/receive`

### Events Published
- `StockTransferShipped`
- `StockTransferReceived`

### Events Consumed
- None

## 10. Notifications
- In-transit aging alerts

## 11. Reports
- Transfer register

## 12. Audit, Retention, and Privacy
Full audit trail mandatory.

## 13. Failure, Idempotency, and Concurrency
- Ship/receive idempotent
- Batch qty constrained

## 14. Non-Functional Requirements
- Standard SLAs

## 15. Dependencies
- Stores/Batches

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| INV-XFER-AC-001 | Shipped stock leaves source and arrives only on receive. |
| INV-XFER-AC-002 | Audit shows actors for ship/receive. |

## 17. Open Assumptions
- Cross-facility transfers may need additional FIN intercompany later.

## 18. Source Traceability
Mapped from `§6.1 transfers; §6.2 step 7` in `Healthcare-ERP-Pathway-and-Workflow.md`.
