# Requirements Verification Package

## Status
Automated consistency checks complete. Open assumptions below are accepted as **default delivery decisions** for scaffolding (per approved delivery plan). Amendments can still be made; they will create ADRs.

| Default decision | Value |
|---|---|
| Tenancy | Single-tenant hospital group, multi-facility |
| Locale pack | Configurable; placeholders for PK-oriented identifiers (CNIC/MRN) |
| Auth | ASP.NET Core Identity + JWT (OIDC-ready) |
| Events | In-process outbox/inbox dispatcher |
| Budget hard-stop | Warn mode by default |
| Portals | Phase 4 |
| Currency | One base currency per facility |
| Target framework | `net10.0` if SDK available; otherwise `net9.0` with TFM bump path documented |

## File Inventory
| Area | Files |
|---|---|
| Index / registers | `README.md`, `TRACEABILITY.md`, `VERIFICATION.md` |
| Foundation | 11 (overview + 10 sub-modules) |
| HMS | 12 (overview + 11 sub-modules) |
| HRIS | 11 (overview + 10 sub-modules) |
| Financials | 9 (overview + 8 sub-modules) |
| Inventory | 10 (overview + 9 sub-modules) |
| Procurement | 10 (overview + 9 sub-modules) |
| Cross-module | 10 (overview + 8 pathways + event catalog) |

## Consistency Checks Performed
| Check | Result |
|---|---|
| Master data ownership unique (Patient HMS, Employee HRIS, Item INV, Vendor PRC, COA/CC FIN, Approvals FND) | Pass |
| Integration triggers from blueprint §§3.3–7.3 represented as events/AC | Pass |
| Cross-module pathways reference existing module events | Pass |
| Approval/RBAC/Audit governance applied across modules | Pass |
| Requirement ID convention applied | Pass |
| No module instructed to write another module's tables | Pass |
| Phasing aligns with blueprint §10 | Pass |

## Open Assumptions Pending Your Decision
1. Initial deployment is single-tenant hospital group (multi-facility supported).
2. Primary locale/statutory pack to be confirmed (tax, payroll, identifiers).
3. Auth starts with built-in OpenIddict/Identity with path to external OIDC.
4. PACS/analyzer/biometric integrations are adapter-based after core workflows.
5. In-process outbox dispatcher for modular monolith MVP (broker optional later).
6. Hard budget control on PO is optional per facility (default warn).
7. Patient portal and vendor portal are Phase 4.
8. Currency: one base currency per facility initially.

## Approval Checklist
- [ ] Glossary and ownership model accepted
- [ ] Foundation requirements accepted
- [ ] HMS requirements accepted (Phase 1 subset can be prioritized)
- [ ] HRIS/FIN/INV/PRC requirements accepted
- [ ] Cross-module event catalog accepted
- [ ] Open assumptions confirmed or amended
- [ ] Authorization to scaffold .NET 10 + React + PostgreSQL modular monolith

## Reviewer Sign-off
| Role | Name | Date | Decision |
|---|---|---|---|
| Product Owner | | | Approve / Amend |
| Architecture | | | Approve / Amend |
| Clinical ops | | | Approve / Amend |
| Finance/HR ops | | | Approve / Amend |
