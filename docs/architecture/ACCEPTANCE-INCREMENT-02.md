# Acceptance Checklist — Increment 2 (Financials + Inventory + Procurement)

## Requirement coverage
| Area | Specs | Implemented |
|---|---|---|
| Chart of accounts / cost centers | FIN-GL-*, FIN-BUD-* | Create/list accounts and cost centers |
| AR open items from HMS charges | FIN-AR-*, XWF-O2C-* | `BillableEventCreated` handler creates receivables |
| AP invoice + three-way match gate | FIN-AP-* | Capture invoice; match requires PO + GRN refs |
| Item/store/stock | INV-ITEM-*, INV-STR-*, INV-ISS-* | Item/store CRUD, receive/issue stock |
| Auto reorder signal | INV-ROP-*, XWF-MED-* | Issue below reorder emits `PurchaseRequisitionRequested` |
| Vendor + PR + PO | PRC-VND-*, PRC-PR-*, PRC-PO-* | Vendor create; auto PR from signal; issue PO |

## Automated verification
- [x] `dotnet test` — 10 tests passed (7 unit, 2 architecture, 1 integration)
- [x] Local Docker stack rebuild via `.\scripts\build-local-docker.ps1`
- [x] `/api/health` healthy on `http://localhost:5080`
- [x] Docker smoke: create facility → FIN account → INV receive/issue → auto PRC requisition

## Known limitations
- HRIS credential gates not enforced yet (Phase 3)
- Batch/FEFO and full GRN quality workflow still pending
- AP payment disbursement and bank file generation pending
- React UI console still covers Foundation/HMS only
- Docker Hub DNS on this machine intermittently blocks Node/Nginx image pulls; UI is optional Compose profile `ui`

## Sign-off
| Role | Decision | Date |
|---|---|---|
| Product Owner | **Approved** | 2026-07-18 |
