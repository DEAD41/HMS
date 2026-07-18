# Shared Master Data Contracts

| Field | Value |
|---|---|
| Module | FND |
| Sub-module | MDM |
| Status | Draft — pending verification |
| Source | §2 |

## 1. Scope
Define canonical reference contracts and ownership rules for Patient, Employee, Item/SKU, Vendor, Chart of Accounts/Cost Centers, and Approval rules so modules share identity without duplicating masters.

## 2. Exclusions
Full golden-record MDM UI beyond ownership/sync contracts in Phase 1.

## 3. Actors and Permissions
- Integration services — publish/consume master reference changes
- Module owners — authoritative CRUD in owning module
- Consuming modules — read-only projections/caches

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| FND-MDM-FR-001 | Each master object shall have exactly one owning module as defined in the ownership table. |
| FND-MDM-FR-002 | Owning module shall publish create/update/deactivate events with stable global IDs. |
| FND-MDM-FR-003 | Consuming modules shall store only reference projections needed for local integrity and display. |
| FND-MDM-FR-004 | Hard deletes of master records are forbidden; only soft-deactivate/archive is allowed. |
| FND-MDM-FR-005 | Cross-module foreign keys shall reference global IDs, never local surrogate IDs of another module. |
| FND-MDM-FR-006 | Master change events shall be versioned and idempotent. |

## 5. Workflow and State Transitions
Ownership:
| Object | Owner | Consumers |
|---|---|---|
| Patient | HMS | FIN, INV |
| Employee | HRIS | HMS, FIN, PRC, FND RBAC |
| Item/SKU | INV | HMS, PRC, FIN |
| Vendor | PRC | FIN, INV |
| COA / Cost Center | FIN | All |
| Approval rules | FND | All |

State for all masters: `Draft -> Active -> Suspended -> Archived`.

## 6. Data / Entities and Validation
- `MasterReference` projection — globalId, ownerModule, type, code, displayName, status, version, lastSyncedAt
- Validation: globalId UUID; code non-empty; status enum enforced

## 7. Business Rules
| ID | Rule |
|---|---|
| FND-MDM-BR-001 | Consumers must not mutate authoritative master attributes. |
| FND-MDM-BR-002 | If owner event version is older than local projection, ignore (idempotent). |
| FND-MDM-BR-003 | Suspended masters cannot be selected in new transactions. |

## 8. Approvals
Master deactivation that impacts open transactions raises warning and may require approval depending on object type.

## 9. APIs and Module Ownership
**Owner:** FND

### APIs
- `GET /api/fnd/master/{type}/{globalId}`
- `GET /api/fnd/master/{type}?query=`
- `POST /api/fnd/master/sync/replay (admin)`

### Events Published
- `MasterProjectionUpdated`

### Events Consumed
- `PatientChanged (HMS)`
- `EmployeeChanged (HRIS)`
- `ItemChanged (INV)`
- `VendorChanged (PRC)`
- `AccountChanged / CostCenterChanged (FIN)`

## 10. Notifications
- Admin alert on sync lag beyond threshold

## 11. Reports
- Master sync health
- Suspended masters in use

## 12. Audit, Retention, and Privacy
Projection sync operations audited. PHI/PII fields minimized in projections; full clinical data remains in HMS.

## 13. Failure, Idempotency, and Concurrency
- Exactly-once effective processing via inbox dedupe on eventId.
- Replay tool can rebuild projections from outbox archive.
- Concurrent consumer updates last-write by version number.

## 14. Non-Functional Requirements
- Projection update lag P95 < 5s under normal load.
- No cross-module direct DB joins in application code.

## 15. Dependencies
- FND Integration Events
- Owning modules for each master

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| FND-MDM-AC-001 | Creating a patient in HMS makes patient selectable in billing/inventory projections. |
| FND-MDM-AC-002 | Suspended vendor cannot be used on new POs. |
| FND-MDM-AC-003 | Architecture tests fail if module references another module's persistence assembly. |

## 17. Open Assumptions
- Projections may cache display fields (name/code/status) only.
- National identifier formats are locale-configurable.

## 18. Source Traceability
Mapped from `§2` in `Healthcare-ERP-Pathway-and-Workflow.md`.
