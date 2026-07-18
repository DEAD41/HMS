# Acceptance Checklist — Increment 1 (Foundation + HMS Core)

## Requirement coverage
| Area | Specs | Implemented |
|---|---|---|
| Facilities / org units | FND-TEN-* | Create/list facility + org units APIs |
| Audit write | FND-AUD-* | AuditWriter on create paths |
| Outbox | FND-EVT-* | Outbox table + background dispatcher |
| Patient registration | HMS-FO-* | Register/search patients |
| Appointments | HMS-FO-* | Schedule/list/check-in |
| OPD | HMS-OPD-* | Open/close encounter |
| Billing charges | HMS-BIL-* | Idempotent charge posting on OPD close |

## Automated verification
- [x] `dotnet test` passes (unit + architecture + integration health)
- [x] `/api/health` returns Healthy
- [x] Can create facility, register patient, schedule appointment, check-in, open/close OPD with charge

## Known limitations
- Auth is stubbed (CurrentUser reads headers/claims; JWT wiring next)
- PostgreSQL migrations not yet generated (`EnsureCreated` used in Docker)
- HRIS credential gate not yet enforced on scheduling
- React UI is a thin operational console for the MVP paths

## Sign-off
| Role | Decision | Date |
|---|---|---|
| Product Owner | **Approved** | 2026-07-18 |
