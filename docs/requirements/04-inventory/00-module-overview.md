# Store & Spares (Inventory) — Module Overview

| Field | Value |
|---|---|
| Module code | `INV` |
| Implementation phase | Phase 2 operations |
| Source | Blueprint §6 |

## Purpose
Item master ownership, multi-store stock control, batch/expiry, issues, transfers, reorder planning, counts, and biomedical spares.

## Sub-modules
| Document | Summary |
|---|---|
| [Stores & Bins](01-stores-bins.md) | Central/sub-stores and bins |
| [Item Master](02-item-master.md) | SKU master |
| [Receipts & Quality](03-receipts-quality.md) | GRN quality and putaway |
| [Batch & Expiry](04-batch-expiry.md) | Batch/FEFO controls |
| [Issues & Consumption](05-issues-consumption.md) | Patient/dept/spares issues |
| [Transfers](06-transfers.md) | Inter-store transfers |
| [Reorder Planning](07-reorder-planning.md) | Min/max and auto PR |
| [Counts & Adjustments](08-counts-adjustments.md) | Cycle counts and variances |
| [Biomedical Spares](09-biomedical-spares.md) | Spares for equipment |

## Master Data Ownership
- Item/SKU master
- Stock ledgers
- Batches
- Stores/bins

## Master Data Consumed
- PRC PO/vendor
- HMS pharmacy/ward/OT issues
- FIN COGS/write-off/asset maintenance
- FND approvals

## Integration Summary
This module publishes domain events through the Foundation integration hub and never writes directly into another module's tables. Cross-module workflows are specified under `06-cross-module-workflows/`.

## Verification Gate
Implementation of this module starts only after:
1. All sub-module requirement files are approved.
2. Foundation contracts used by this module are approved.
3. Acceptance criteria IDs are linked in the traceability register.
