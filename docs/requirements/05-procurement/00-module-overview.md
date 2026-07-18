# Procurement — Module Overview

| Field | Value |
|---|---|
| Module code | `PRC` |
| Implementation phase | Phase 2 operations |
| Source | Blueprint §7 |

## Purpose
Procure-to-pay front office: vendors, requisitions, RFQ/tenders, contracts, purchase orders, GRN coordination, and vendor performance.

## Sub-modules
| Document | Summary |
|---|---|
| [Purchase Requisitions](01-requisitions.md) | Manual and auto PR |
| [Procurement Approvals](02-approvals.md) | Value-based approval routing |
| [Vendor Management](03-vendors.md) | Vendor master ownership |
| [RFQ / Tendering](04-rfq-tenders.md) | Sourcing events |
| [Quote Comparison](05-quote-comparison.md) | Award decisions |
| [Contracts & Rate Contracts](06-contracts.md) | Rate contracts |
| [Purchase Orders](07-purchase-orders.md) | PO issuance |
| [Goods Receipt Coordination](08-receipt-coordination.md) | PO-GRN collaboration |
| [Vendor Performance & Compliance](09-vendor-performance.md) | Scorecards and certificates |

## Master Data Ownership
- Vendor master
- Requisitions
- RFQs
- Contracts
- Purchase orders

## Master Data Consumed
- INV reorder/items/GRN
- HRIS org for approvals
- FIN AP/assets
- FND approvals engine

## Integration Summary
This module publishes domain events through the Foundation integration hub and never writes directly into another module's tables. Cross-module workflows are specified under `06-cross-module-workflows/`.

## Verification Gate
Implementation of this module starts only after:
1. All sub-module requirement files are approved.
2. Foundation contracts used by this module are approved.
3. Acceptance criteria IDs are linked in the traceability register.
