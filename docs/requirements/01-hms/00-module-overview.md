# Hospital Management System (HMS) — Module Overview

| Field | Value |
|---|---|
| Module code | `HMS` |
| Implementation phase | Phase 1 core (registration/OPD/billing); Phase 2 operational sub-modules |
| Source | Blueprint §3 |

## Purpose
Manage the patient clinical and administrative pathway from registration through discharge and follow-up, integrating with Inventory, Financials, and HRIS credential gates.

## Sub-modules
| Document | Summary |
|---|---|
| [Front Office](01-front-office.md) | Appointments, registration, insurance/TPA verification |
| [OPD](02-opd.md) | Outpatient encounters and consultation |
| [IPD / Bed / Nursing](03-ipd-bed-nursing.md) | Admission, beds, nursing, MAR, consumables |
| [Emergency & Triage](04-emergency-triage.md) | Triage routing and emergency care |
| [Operation Theatre](05-ot.md) | OT scheduling, checklists, implant/consumable usage |
| [Laboratory (LIS)](06-lis.md) | Lab orders, samples, results |
| [Radiology / RIS-PACS](07-ris-pacs.md) | Imaging orders, reports, PACS link |
| [Pharmacy](08-pharmacy.md) | Inpatient and retail dispense |
| [Medical Records (EMR/EHR)](09-emr-ehr.md) | Clinical documentation and orders |
| [Billing & Claims](10-billing-claims.md) | Charges, bills, insurance claims |
| [Discharge & Follow-up](11-discharge-follow-up.md) | Discharge summary, follow-up, portal handoff |

## Master Data Ownership
- Patient master
- Encounters
- Clinical orders
- EMR documents
- Bills/claims (originating)

## Master Data Consumed
- Employee/credentials (HRIS)
- Item stock availability (INV)
- COA/cost centers (FIN)
- Approvals/RBAC (FND)

## Integration Summary
This module publishes domain events through the Foundation integration hub and never writes directly into another module's tables. Cross-module workflows are specified under `06-cross-module-workflows/`.

## Verification Gate
Implementation of this module starts only after:
1. All sub-module requirement files are approved.
2. Foundation contracts used by this module are approved.
3. Acceptance criteria IDs are linked in the traceability register.
