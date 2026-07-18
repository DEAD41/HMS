# Cross-Module Workflows — Overview

| Field | Value |
|---|---|
| Module code | `XWF` |
| Source | Blueprint §§3.3, 4.3, 5.3, 6.3, 7.3, 8 |

## Purpose
Specify end-to-end choreography across modules, including canonical events, failure handling, and reconciliation expectations.

## Documents
| Document | Pathway |
|---|---|
| [Medication to Replenishment](01-medication-to-replenishment.md) | HMS order → INV issue → reorder → PRC PO → GRN → availability |
| [Procure to Pay](02-procure-to-pay.md) | PR → PO → GRN → AP match → payment |
| [Order to Cash](03-order-to-cash.md) | HMS charges → invoice → AR → receipt |
| [Hire to Retire](04-hire-to-retire.md) | Recruit → credential → schedule → exit/revoke |
| [Payroll Posting](05-payroll-posting.md) | HRIS payroll → FIN GL/bank |
| [Equipment Maintenance](06-equipment-maintenance.md) | Fault → spare issue → asset cost/depreciation |
| [Discharge to Claim](07-discharge-to-claim.md) | Discharge → final bill → claim → settlement |
| [Canonical Events & Reconciliation](08-canonical-events-reconciliation.md) | Event catalog, errors, reconciliation |

## Rule
No cross-module synchronous distributed transactions across databases/schemas. Use outbox events, idempotent handlers, and compensating actions.
