# Vendor Management

| Field | Value |
|---|---|
| Module | PRC |
| Sub-module | VND |
| Status | Draft — pending verification |
| Source | §7.1 vendor management; §2 vendor ownership |

## 1. Scope
Vendor registration, onboarding documents, banking, categories, and status for purchasing/AP.

## 2. Exclusions
Full SRM social collaboration network.

## 3. Actors and Permissions
- Vendor Master Steward
- Buyer
- AP Clerk (read)
- Compliance

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| PRC-VND-FR-001 | Register vendors with legal and tax identifiers. |
| PRC-VND-FR-002 | Capture banking and contact details securely. |
| PRC-VND-FR-003 | Track regulatory certificates for medical supplies. |
| PRC-VND-FR-004 | Activate/suspend vendors and publish VendorChanged. |
| PRC-VND-FR-005 | Support evaluation score inputs from performance module. |

## 5. Workflow and State Transitions
Vendor: `Draft -> UnderReview -> Active -> Suspended -> Blacklisted | Archived`.

## 6. Data / Entities and Validation
- `Vendor`
- `VendorSite`
- `VendorBankAccount`
- `VendorCertificate`

## 7. Business Rules
| ID | Rule |
|---|---|
| PRC-VND-BR-001 | Suspended/blacklisted vendors cannot receive new POs. |
| PRC-VND-BR-002 | Certificate expiry can auto-suspend category purchasing. |

## 8. Approvals
Blacklisting requires Compliance/Finance approval.

## 9. APIs and Module Ownership
**Owner:** PRC

### APIs
- `POST /api/prc/vendors`
- `PUT /api/prc/vendors/{id}`
- `POST /api/prc/vendors/{id}/certificates`

### Events Published
- `VendorChanged`
- `VendorSuspended`

### Events Consumed
- None

## 10. Notifications
- Certificate expiry alerts

## 11. Reports
- Vendor master
- Certificate compliance

## 12. Audit, Retention, and Privacy
Vendor banking PII/sensitive; masked in UI; access audited.

## 13. Failure, Idempotency, and Concurrency
- Update optimistic concurrency
- Event outbox

## 14. Non-Functional Requirements
- Vendor search P95 < 300ms

## 15. Dependencies
- FIN AP
- INV GRN
- Docs
- Performance

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| PRC-VND-AC-001 | Active vendor selectable on PO. |
| PRC-VND-AC-002 | Expired pharma certificate blocks PO for that category when policy enabled. |

## 17. Open Assumptions
- Tax ID validation rules locale-specific.

## 18. Source Traceability
Mapped from `§7.1 vendor management; §2 vendor ownership` in `Healthcare-ERP-Pathway-and-Workflow.md`.
