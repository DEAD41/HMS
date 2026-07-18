# Acceptance Checklist — Increment 6 (Clinical Depth)

## Requirement coverage
| Area | Specs | Implemented |
|---|---|---|
| INV batch + FEFO | INV-BCH-*, HMS-PHX-BR-002 | `Batch` receive/issue; FEFO allocation; expired reject |
| Pharmacy → FEFO stock | HMS-PHX-FR-002/004, XWF-MED-* | `MedicationDispensed` handler calls INV FEFO `IssueAsync` |
| Nursing care plan | HMS-IPD-FR-003 | `POST /api/hms/ipd/care-plans` |
| MAR | HMS-IPD-FR-004, AC-002 | `POST /api/hms/ipd/mar`; administered immutable; nurse credential gate |
| LIS stub adapter | HMS-LIS-* | Sample collect + analyzer import → finalize |
| RIS stub adapter | HMS-RIS-* | PACS stub acquire (`StudyInstanceUid`) → sign |

## Automated verification
- [x] `dotnet test` — 25 tests passed (22 unit, 2 architecture, 1 integration)
- [x] Local Docker rebuild via `.\scripts\build-local-docker.ps1` (with `docker compose down -v`)
- [x] Smoke: batch-controlled receive (2 lots) → pharmacy dispense → earlier-expiry batch reduced
- [x] Smoke: admit → care plan → dispense → MAR administer (nurse credential); duplicate dose rejected
- [x] Smoke: lab adapter import → finalize; rad adapter acquire → sign

## Known limitations
- No EF migrations yet (volume reset required for schema changes)
- Real HL7 analyzer / DICOM PACS middleware deferred (stubs only)
- Ward consumables + full EMR/CPOE deferred
- Production auth hardening deferred (separate track)

## Sign-off
| Role | Decision | Date |
|---|---|---|
| Product Owner | Pending | |
