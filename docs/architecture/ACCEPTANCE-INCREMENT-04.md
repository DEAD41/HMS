# Acceptance Checklist — Increment 4 (HRIS)

## Requirement coverage
| Area | Specs | Implemented |
|---|---|---|
| Employee master | HRIS-EMP-* | Create, activate, exit; `EmployeeChanged` / `EmployeeExited` |
| Credentialing | HRIS-CRD-* | Add credential (Submitted), verify → Active; `EmployeeCredentialStatusChanged` |
| Roster | HRIS-RST-* | Publish roster; clinical dept requires schedulable credentials |
| Leave | HRIS-LV-* | Submit + approve; overlap guard on approved leave |
| Payroll | HRIS-PAY-*, XWF-PAY-* | Create run, post → `PayrollPosted` → FIN `PayrollExpense` |
| HMS credential gate | XWF-HIRE / HMS scheduling | Appointment + OT schedule blocked without active verified credentials |

## Automated verification
- [x] `dotnet test` — 17 tests passed (14 unit, 2 architecture, 1 integration)
- [x] Local Docker rebuild via `.\scripts\build-local-docker.ps1` (with `docker compose down -v` for new HRIS DB)
- [x] Smoke: create/activate employee → add/verify credential → schedule appointment allowed
- [x] Smoke: schedule appointment without verified credential → blocked
- [x] Smoke: post payroll → FIN `/api/fin/payroll-expenses` shows expense

## Known limitations
- Recruitment / onboarding workflows simplified to employee create + activate
- Attendance clock-in and full payroll statutory calculations deferred
- Self-service portal deferred
- React UI does not yet cover HRIS screens

## Sign-off
| Role | Decision | Date |
|---|---|---|
| Product Owner | **Approved** | 2026-07-18 |
