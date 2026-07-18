# Foundation / Integration Hub — Module Overview

| Field | Value |
|---|---|
| Module code | `FND` |
| Implementation phase | Phase 1 (must be first) |
| Source | Blueprint §§2, 9 |

## Purpose
Provides shared platform capabilities and master-data contracts so HMS, HRIS, Financials, Inventory, and Procurement never couple directly.

## Sub-modules
| Document | Summary |
|---|---|
| [Tenancy & Facilities](01-tenancy-facilities.md) | Hospitals, sites, departments, wards |
| [Shared Master Data](02-shared-master-data.md) | Cross-module identity of patient/employee/item/vendor/COA references |
| [Identity & RBAC](03-identity-rbac.md) | Users, roles, permissions, session policy |
| [Approval Workflows](04-approval-workflows.md) | Configurable approval engine |
| [Audit & Compliance](05-audit-compliance.md) | Immutable audit trail and retention |
| [Notifications](06-notifications.md) | In-app, email, SMS hooks |
| [Document Storage](07-document-storage.md) | Secure document vault |
| [Integration Events](08-integration-events.md) | Outbox/inbox event bus |
| [Reporting Contracts](09-reporting.md) | Unified MIS/BI extract contracts |
| [Data Governance](10-data-governance.md) | Privacy, retention, consent, residency |

## Master Data Ownership
- Facility/tenant structure
- User identity and role model
- Approval workflow definitions
- Audit store
- Notification and document services
- Event infrastructure

## Master Data Consumed
- Module-owned masters via reference IDs (patient, employee, item, vendor, COA)

## Integration Summary
This module publishes domain events through the Foundation integration hub and never writes directly into another module's tables. Cross-module workflows are specified under `06-cross-module-workflows/`.

## Verification Gate
Implementation of this module starts only after:
1. All sub-module requirement files are approved.
2. Foundation contracts used by this module are approved.
3. Acceptance criteria IDs are linked in the traceability register.
