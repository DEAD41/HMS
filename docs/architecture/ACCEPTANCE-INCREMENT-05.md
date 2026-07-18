# Acceptance Checklist — Increment 5 (Phase 4 Optimization)

## Requirement coverage
| Area | Specs | Implemented |
|---|---|---|
| Identity / login | FND-IAM-* | JWT login, roles, seeded demo users, `/api/fnd/auth/*` |
| Budgeting / cost centers | FIN-BUD-* | Budget lines create/activate/actuals + variance API |
| MIS / KPIs | FIN-MIS-* | `/api/fin/mis/dashboard` (AR/AP/payroll/budget/cost-per-patient) |
| Vendor performance | PRC-VPR-* | Publish/list vendor scorecards from PO history |
| ESS portal | HRIS-ESS-* | `/api/hris/ess/me`, `/api/hris/ess/leave` (requires employee link) |
| React console | portals | Login screen + Operations / MIS / Self-service tabs |

## Sample users (seeded on API startup)
| Username | Password | Roles |
|---|---|---|
| `admin` | `Admin@123` | Admin, Finance, Hr, Clinician, Employee |
| `doctor` | `Doctor@123` | Clinician, Employee |
| `hr` | `Hr@123` | Hr, Employee |
| `finance` | `Finance@123` | Finance, Employee |
| `employee` | `Employee@123` | Employee |

Also available at `GET /api/fnd/auth/demo-users`.

## Automated verification
- [x] `dotnet test` — 20 tests passed (17 unit, 2 architecture, 1 integration)
- [x] Local Docker rebuild via `.\scripts\build-local-docker.ps1` (with `docker compose down -v`)
- [x] Smoke: login as `admin` → create facility → MIS dashboard returns KPIs
- [x] Smoke: create employee → link to `employee` user → ESS `/api/hris/ess/me` works with token
- [x] Smoke: vendor + PO → publish scorecard

## Known limitations
- Auth is available but most operational APIs remain anonymously callable (JWT required only for `/me`, ESS, user admin)
- Password hashing is SHA-256 demo-grade (not production Identity)
- Vendor on-time/quality KPIs are synthetic until GRN/QC events exist
- Patient portal and full mobile ESS UX deferred
- React UI still a thin console (not full module coverage)

## Sign-off
| Role | Decision | Date |
|---|---|---|
| Product Owner | **Approved** | 2026-07-18 |
