# Taxation & Statutory Reporting

| Field | Value |
|---|---|
| Module | FIN |
| Sub-module | TAX |
| Status | Draft — pending verification |
| Source | §5.1 Taxation & statutory reporting |

## 1. Scope
Tax configuration (sales/withholding/VAT/GST as applicable) and statutory report generation.

## 2. Exclusions
Government e-filing robot beyond export files.

## 3. Actors and Permissions
- Tax Accountant
- Finance Controller

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| FIN-TAX-FR-001 | Configure tax codes/rates and applicability rules. |
| FIN-TAX-FR-002 | Calculate tax on invoices/payments as configured. |
| FIN-TAX-FR-003 | Produce statutory reports/exports for filing periods. |
| FIN-TAX-FR-004 | Support withholding tax on vendor payments where required. |

## 5. Workflow and State Transitions
TaxPeriodReturn: `Open -> Prepared -> Submitted -> Amended`.

## 6. Data / Entities and Validation
- `TaxCode`
- `TaxRate`
- `TaxTransaction`
- `StatutoryReturn`

## 7. Business Rules
| ID | Rule |
|---|---|
| FIN-TAX-BR-001 | Posted tax amounts change only via amending documents. |
| FIN-TAX-BR-002 | Rate changes effective-dated. |

## 8. Approvals
Return submission mark-off may require Controller approval.

## 9. APIs and Module Ownership
**Owner:** FIN

### APIs
- `POST /api/fin/tax/codes`
- `GET /api/fin/tax/returns/{period}`
- `POST /api/fin/tax/returns/{period}/prepare`

### Events Published
- `TaxReturnPrepared`

### Events Consumed
- `InvoiceFinalized`
- `ApPaymentDisbursed`

## 10. Notifications
- Filing deadline reminders

## 11. Reports
- Tax return drafts
- Withholding summaries

## 12. Audit, Retention, and Privacy
Statutory archives retained per law.

## 13. Failure, Idempotency, and Concurrency
- Prepare job idempotent per period version

## 14. Non-Functional Requirements
- Prepare month return within batch SLA

## 15. Dependencies
- FIN AR/AP/GL

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| FIN-TAX-AC-001 | Invoice tax calculated using active rates. |
| FIN-TAX-AC-002 | Period return includes posted tax transactions. |

## 17. Open Assumptions
- Locale tax pack selected at deployment.

## 18. Source Traceability
Mapped from `§5.1 Taxation & statutory reporting` in `Healthcare-ERP-Pathway-and-Workflow.md`.
