# Pharmacy (In-patient and Retail)

| Field | Value |
|---|---|
| Module | HMS |
| Sub-module | PHX |
| Status | Draft — pending verification |
| Source | §3.1 Pharmacy; §3.2 medication fulfillment; §3.3 dispense -> inventory |

## 1. Scope
Medication order verification, dispensing from Inventory stock, patient counseling/retail sales, and charge posting.

## 2. Exclusions
Robotics/cabinet device control; full clinical decision support beyond basic interactions in MVP.

## 3. Actors and Permissions
- Pharmacist
- Pharmacy Technician
- Retail Cashier
- Ordering Clinician

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HMS-PHX-FR-001 | Receive medication orders and perform pharmacist verification. |
| HMS-PHX-FR-002 | Allocate batches via FEFO from configured pharmacy stores. |
| HMS-PHX-FR-003 | Dispense inpatient and retail prescriptions with labeling data. |
| HMS-PHX-FR-004 | Decrement Inventory stock through integration events/commands. |
| HMS-PHX-FR-005 | Auto-post medication charges to patient bill / retail receipt. |
| HMS-PHX-FR-006 | Support returns/wastage with reason codes. |

## 5. Workflow and State Transitions
Med order pharmacy state: `New -> Verified -> PartiallyDispensed -> Dispensed | Rejected | Cancelled`.
Dispense: `Posted` immutable except return document.

## 6. Data / Entities and Validation
- `MedicationOrder`
- `DispenseTransaction`
- `DispenseLine(batch)`
- `PharmacyReturn`

## 7. Business Rules
| ID | Rule |
|---|---|
| HMS-PHX-BR-001 | Cannot dispense more than ordered without amendment. |
| HMS-PHX-BR-002 | Expired batches cannot be dispensed. |
| HMS-PHX-BR-003 | Credentialed pharmacist required for verification where policy mandates. |
| HMS-PHX-BR-004 | Below-reorder resulting stock triggers procurement requisition via Inventory rules. |

## 8. Approvals
High-value controlled drug dispense may require dual verification/approval.

## 9. APIs and Module Ownership
**Owner:** HMS

### APIs
- `POST /api/hms/pharmacy/orders/{id}/verify`
- `POST /api/hms/pharmacy/dispense`
- `POST /api/hms/pharmacy/returns`

### Events Published
- `MedicationDispensed`
- `MedicationReturned`
- `BillableEventCreated`

### Events Consumed
- `ClinicalOrderPlaced`
- `StockAvailabilityChanged`
- `ItemChanged`

## 10. Notifications
- Out-of-stock to clinician
- Controlled drug dual-verify prompts

## 11. Reports
- Dispense volume
- Substitution log
- Controlled drug register

## 12. Audit, Retention, and Privacy
Dispense records immutable and highly regulated; retention extended for controlled substances as configured.

## 13. Failure, Idempotency, and Concurrency
- Dispense posting uses idempotency key and stock reservation to avoid oversell.
- Concurrent dispenses serialize per batch.

## 14. Non-Functional Requirements
- Dispense confirm P95 < 500ms excluding printer

## 15. Dependencies
- INV stock/batches
- HMS Billing/EMR/MAR
- FIN revenue posting
- HRIS credentials

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HMS-PHX-AC-001 | Successful dispense reduces stock and adds charge. |
| HMS-PHX-AC-002 | Expired batch rejected at allocation. |
| HMS-PHX-AC-003 | Reorder breach after dispense creates purchase requisition (via INV). |

## 17. Open Assumptions
- Drug-drug interaction engine can be rules-lite initially.

## 18. Source Traceability
Mapped from `§3.1 Pharmacy; §3.2 medication fulfillment; §3.3 dispense -> inventory` in `Healthcare-ERP-Pathway-and-Workflow.md`.
