# Traceability Register

| Requirement ID pattern | Spec location | Design artifact | Code | Tests |
|---|---|---|---|---|
| FND-*-FR/BR/AC | `docs/requirements/00-foundation/` | ADR-001, ACCEPTANCE-01 | `src/Modules/Foundation` | Unit + architecture + Docker health |
| HMS-FO/OPD/BIL-* | `docs/requirements/01-hms/` | ACCEPTANCE-01 | `src/Modules/Hms` + API controllers | Unit + integration health |
| FIN-GL/AR/AP-* | `docs/requirements/03-financials/` | ACCEPTANCE-02 | `src/Modules/Financials` | Unit domain tests |
| INV-ITEM/STR/ISS/ROP-* | `docs/requirements/04-inventory/` | ACCEPTANCE-02 | `src/Modules/Inventory` | Unit + Docker smoke (issue→PR) |
| PRC-VND/PR/PO-* | `docs/requirements/05-procurement/` | ACCEPTANCE-02 | `src/Modules/Procurement` | Unit + Docker smoke (auto PR) |
| XWF-MED/O2C/P2P-* | `docs/requirements/06-cross-module-workflows/` | Event catalog | Outbox handlers in FIN/PRC | Docker smoke |
| HRIS-*, remaining HMS ops | `docs/requirements/02-hris/`, `01-hms/` | Pending next gated increment | Module shells present | Pending |

## Update Rule
When implementing a requirement, append concrete file/test links under the matching module section or acceptance checklist.
