# General Ledger / Chart of Accounts

| Field | Value |
|---|---|
| Module | FIN |
| Sub-module | GL |
| Status | Draft — pending verification |
| Source | §5.1 GL/COA; all postings |

## 1. Scope
Maintain COA, accounting periods, journals, and financial postings from all modules.

## 2. Exclusions
Multi-GAAP consolidation group accounting beyond single primary book MVP.

## 3. Actors and Permissions
- Accountant
- Finance Controller

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| FIN-GL-FR-001 | Maintain chart of accounts and account types. |
| FIN-GL-FR-002 | Open/close accounting periods. |
| FIN-GL-FR-003 | Post manual and system journals with balanced debits/credits. |
| FIN-GL-FR-004 | Provide trial balance and account inquiry. |
| FIN-GL-FR-005 | Support cost center dimensions on postings. |

## 5. Workflow and State Transitions
Period: `Future -> Open -> SoftClose -> Closed`.
Journal: `Draft -> Posted | Reversed`.

## 6. Data / Entities and Validation
- `Account`
- `AccountingPeriod`
- `JournalEntry`
- `JournalLine`

## 7. Business Rules
| ID | Rule |
|---|---|
| FIN-GL-BR-001 | Posted journals immutable; corrections via reversing entries. |
| FIN-GL-BR-002 | Journals must balance in transaction currency/base currency rules. |
| FIN-GL-BR-003 | Closed periods reject new postings except controlled reopen. |

## 8. Approvals
Period close and reopen require Controller approval.

## 9. APIs and Module Ownership
**Owner:** FIN

### APIs
- `POST /api/fin/coa/accounts`
- `POST /api/fin/journals`
- `POST /api/fin/periods/{id}/close`

### Events Published
- `AccountChanged`
- `JournalPosted`
- `PeriodClosed`

### Events Consumed
- `PayrollPosted`
- `InvoiceFinalized`
- `VendorInvoiceMatched`
- `StockIssued`
- `StockWrittenOff`
- `FnFPosted`

## 10. Notifications
- Period close reminders

## 11. Reports
- Trial balance
- Journal register

## 12. Audit, Retention, and Privacy
Financial records statutory retention; immutable posted ledger.

## 13. Failure, Idempotency, and Concurrency
- System posting idempotent by sourceDocumentId
- Concurrent period close guarded

## 14. Non-Functional Requirements
- Posting P95 < 200ms

## 15. Dependencies
- All feeder modules
- FND Approvals

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| FIN-GL-AC-001 | Unbalanced journal rejected. |
| FIN-GL-AC-002 | Duplicate sourceDocumentId does not double post. |

## 17. Open Assumptions
- Single base currency per facility with optional multi-currency later.

## 18. Source Traceability
Mapped from `§5.1 GL/COA; all postings` in `Healthcare-ERP-Pathway-and-Workflow.md`.
