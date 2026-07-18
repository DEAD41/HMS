# Financials — Module Overview

| Field | Value |
|---|---|
| Module code | `FIN` |
| Implementation phase | Phase 1 core GL/AP/AR; Phase 4 budgeting/advanced MIS |
| Source | Blueprint §5 |

## Purpose
General ledger and financial operations covering order-to-cash, procure-to-pay, payroll posting, budgeting, assets, tax, and MIS.

## Sub-modules
| Document | Summary |
|---|---|
| [GL / Chart of Accounts](01-gl-coa.md) | COA, journals, periods |
| [Accounts Payable](02-ap.md) | Vendor invoices, three-way match, payments |
| [Accounts Receivable](03-ar.md) | Patient/insurer receivables |
| [Budgeting & Cost Centers](04-budgeting-cost-centers.md) | Budgets and control |
| [Fixed Assets](05-fixed-assets.md) | Assets and depreciation |
| [Cash & Bank](06-cash-bank.md) | Cash/bank management |
| [Tax & Statutory](07-tax-statutory.md) | Tax configuration and statutory reports |
| [MIS & Financial Reporting](08-mis.md) | P&L, BS, cost-per-patient, profitability |

## Master Data Ownership
- Chart of accounts
- Cost centers
- GL
- AP/AR subledgers
- Fixed assets
- Tax config

## Master Data Consumed
- HMS billing events
- INV consumption/write-offs
- PRC PO/GRN/vendor
- HRIS payroll
- FND approvals

## Integration Summary
This module publishes domain events through the Foundation integration hub and never writes directly into another module's tables. Cross-module workflows are specified under `06-cross-module-workflows/`.

## Verification Gate
Implementation of this module starts only after:
1. All sub-module requirement files are approved.
2. Foundation contracts used by this module are approved.
3. Acceptance criteria IDs are linked in the traceability register.
