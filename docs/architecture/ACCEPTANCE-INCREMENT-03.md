# Acceptance Checklist — Increment 3 (HMS Operational Sub-modules)

## Requirement coverage
| Area | Specs | Implemented |
|---|---|---|
| IPD beds / admission | HMS-IPD-* | Create beds, admit patient, occupy bed, bed-day charge |
| Emergency & triage | HMS-ER-* | Open ER (incl. unidentified auto `UNK-*`), triage, dispose |
| Operation theatre | HMS-OT-* | Schedule, checklist gate, complete + procedure charge |
| Laboratory (LIS) | HMS-LIS-* | Accept order, finalize result, charge, `LabResultPosted` |
| Radiology (RIS) | HMS-RIS-* | Accept study, sign report, charge, `RadiologyReportPosted` |
| Pharmacy dispense | HMS-PHX-* | Dispense + charge + `MedicationDispensed` → Inventory issue |
| Discharge & follow-up | HMS-DIS-* | Discharge summary, release bed, optional follow-up appointment |

## Automated verification
- [x] `dotnet test` — 14 tests passed (11 unit, 2 architecture, 1 integration)
- [x] Local Docker rebuild via `.\scripts\build-local-docker.ps1`
- [x] Smoke: admit + bed charge; pharmacy dispense + MED charge; lab finalize; discharge releases bed + follow-up appointment
- [x] Smoke: unidentified ER patient auto-ID + triage (`ESI-2`)

## Known limitations
- Nursing MAR / care plans not yet implemented
- OT implant/batch capture simplified (charge only)
- LIS/RIS device/PACS adapters deferred
- Pharmacy FEFO allocation remains inventory-side (not batch-level on dispense payload)
- Credential gates still pending HRIS increment

## Sign-off
| Role | Decision | Date |
|---|---|---|
| Product Owner | **Approved** | 2026-07-18 |
