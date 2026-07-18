# Tenancy & Facilities

| Field | Value |
|---|---|
| Module | FND |
| Sub-module | TEN |
| Status | Draft — pending verification |
| Source | §1, §2, §9 |

## 1. Scope
Support multi-department hospital or hospital group with sites, departments, wards, cost-center linkage, and facility-scoped configuration.

## 2. Exclusions
Multi-tenant SaaS billing; franchise franchisee commercial management.

## 3. Actors and Permissions
- System Administrator — manage tenants/facilities
- Facility Admin — manage departments/wards for assigned facility
- All authenticated users — read authorized org structure

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| FND-TEN-FR-001 | System shall support one or more facilities under an enterprise tenant. |
| FND-TEN-FR-002 | System shall model departments, wards, clinics, stores, and theatres as organizational units. |
| FND-TEN-FR-003 | Each organizational unit shall optionally map to a Financials cost center reference. |
| FND-TEN-FR-004 | Users and transactional data shall be scoped by facility unless enterprise role grants cross-facility access. |
| FND-TEN-FR-005 | Facility configuration shall allow enabling/disabling modules and sub-modules without schema breakage. |
| FND-TEN-FR-006 | Deactivated organizational units shall be retained for history and blocked from new assignments. |

## 5. Workflow and State Transitions
```
Draft -> Active -> Inactive -> Archived
```
- Draft units are not selectable in operational transactions.
- Inactive units reject new links but keep historical references valid.

## 6. Data / Entities and Validation
- `Tenant` — id, legal name, status
- `Facility` — id, tenantId, code, name, timezone, currency, status
- `OrgUnit` — id, facilityId, type(Department|Ward|Clinic|Store|Theatre|Other), parentId, costCenterRef?, status
- Validation: codes unique per parent; timezone IANA; currency ISO-4217

## 7. Business Rules
| ID | Rule |
|---|---|
| FND-TEN-BR-001 | A user without cross-facility permission cannot read another facility's operational data. |
| FND-TEN-BR-002 | Cost center mapping is optional at create but required before financial postings from that unit. |

## 8. Approvals
Creation/update of facilities requires System Administrator approval workflow when change-control mode is enabled; otherwise direct admin privilege.

## 9. APIs and Module Ownership
**Owner:** FND

### APIs
- `POST /api/fnd/tenants`
- `GET/POST/PUT /api/fnd/facilities`
- `GET/POST/PUT /api/fnd/org-units`

### Events Published
- `FacilityCreated`
- `OrgUnitChanged`

### Events Consumed
- None

## 10. Notifications
- Notify Facility Admins on facility activation/deactivation

## 11. Reports
- Facility hierarchy listing
- Active units by type

## 12. Audit, Retention, and Privacy
All create/update/deactivate actions audited with actor, timestamp, before/after values. Retention per data-governance policy (default 7 years).

## 13. Failure, Idempotency, and Concurrency
- Optimistic concurrency via row version on Facility/OrgUnit.
- Idempotent create using client requestId.
- Reject orphan parent changes that would create cycles.

## 14. Non-Functional Requirements
- Org hierarchy read P95 < 200ms for 2,000 units.
- Support at least 50 facilities per tenant.

## 15. Dependencies
- FND Identity/RBAC
- FIN cost center references (soft)

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| FND-TEN-AC-001 | Admin can create facility and nested department/ward structure. |
| FND-TEN-AC-002 | Inactive ward cannot be selected for new IPD admissions. |
| FND-TEN-AC-003 | Cost-center-linked unit is visible to Financials mapping APIs. |

## 17. Open Assumptions
- Initial deployment is single-tenant hospital group unless specified otherwise.
- Default currency and locale are configurable per facility.

## 18. Source Traceability
Mapped from `§1, §2, §9` in `Healthcare-ERP-Pathway-and-Workflow.md`.
