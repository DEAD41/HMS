#!/usr/bin/env python3
"""Generate complete Healthcare ERP requirements library from the blueprint."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "docs" / "requirements"


def write(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def req_file(
    title: str,
    module_code: str,
    sub_code: str,
    source_refs: str,
    scope: str,
    exclusions: str,
    actors: list[str],
    functional: list[str],
    workflow: str,
    entities: list[str],
    business_rules: list[str],
    approvals: str,
    apis: list[str],
    events_out: list[str],
    events_in: list[str],
    notifications: list[str],
    reports: list[str],
    audit: str,
    failures: list[str],
    nfr: list[str],
    dependencies: list[str],
    acceptance: list[str],
    assumptions: list[str],
) -> str:
    fr_lines = "\n".join(
        f"| {module_code}-{sub_code}-FR-{i:03d} | {text} |"
        for i, text in enumerate(functional, 1)
    )
    actor_lines = "\n".join(f"- {a}" for a in actors)
    entity_lines = "\n".join(f"- {e}" for e in entities)
    br_lines = "\n".join(
        f"| {module_code}-{sub_code}-BR-{i:03d} | {text} |"
        for i, text in enumerate(business_rules, 1)
    )
    api_lines = "\n".join(f"- `{a}`" for a in apis)
    eo = "\n".join(f"- `{e}`" for e in events_out) or "- None"
    ei = "\n".join(f"- `{e}`" for e in events_in) or "- None"
    notif = "\n".join(f"- {n}" for n in notifications) or "- None"
    rep = "\n".join(f"- {r}" for r in reports) or "- None"
    fail = "\n".join(f"- {f}" for f in failures)
    nfr_lines = "\n".join(f"- {n}" for n in nfr)
    dep = "\n".join(f"- {d}" for d in dependencies)
    acc = "\n".join(
        f"| {module_code}-{sub_code}-AC-{i:03d} | {text} |"
        for i, text in enumerate(acceptance, 1)
    )
    assump = "\n".join(f"- {a}" for a in assumptions) or "- None"

    return f"""# {title}

| Field | Value |
|---|---|
| Module | {module_code} |
| Sub-module | {sub_code} |
| Status | Draft — pending verification |
| Source | {source_refs} |

## 1. Scope
{scope}

## 2. Exclusions
{exclusions}

## 3. Actors and Permissions
{actor_lines}

## 4. Functional Requirements
| ID | Requirement |
|---|---|
{fr_lines}

## 5. Workflow and State Transitions
{workflow}

## 6. Data / Entities and Validation
{entity_lines}

## 7. Business Rules
| ID | Rule |
|---|---|
{br_lines}

## 8. Approvals
{approvals}

## 9. APIs and Module Ownership
**Owner:** {module_code}

### APIs
{api_lines}

### Events Published
{eo}

### Events Consumed
{ei}

## 10. Notifications
{notif}

## 11. Reports
{rep}

## 12. Audit, Retention, and Privacy
{audit}

## 13. Failure, Idempotency, and Concurrency
{fail}

## 14. Non-Functional Requirements
{nfr_lines}

## 15. Dependencies
{dep}

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
{acc}

## 17. Open Assumptions
{assump}

## 18. Source Traceability
Mapped from `{source_refs}` in `Healthcare-ERP-Pathway-and-Workflow.md`.
"""


def overview(
    title: str,
    code: str,
    purpose: str,
    submodules: list,
    owns: list[str],
    consumes: list[str],
    phase: str,
    source: str,
) -> str:
    rows = "\n".join(
        f"| [{s[0]}]({s[1]}) | {s[2] if len(s) > 2 else ''} |" for s in submodules
    )
    owns_s = "\n".join(f"- {o}" for o in owns)
    cons_s = "\n".join(f"- {c}" for c in consumes)
    return f"""# {title} — Module Overview

| Field | Value |
|---|---|
| Module code | `{code}` |
| Implementation phase | {phase} |
| Source | {source} |

## Purpose
{purpose}

## Sub-modules
| Document | Summary |
|---|---|
{rows}

## Master Data Ownership
{owns_s}

## Master Data Consumed
{cons_s}

## Integration Summary
This module publishes domain events through the Foundation integration hub and never writes directly into another module's tables. Cross-module workflows are specified under `06-cross-module-workflows/`.

## Verification Gate
Implementation of this module starts only after:
1. All sub-module requirement files are approved.
2. Foundation contracts used by this module are approved.
3. Acceptance criteria IDs are linked in the traceability register.
"""


# ---------------------------------------------------------------------------
# README
# ---------------------------------------------------------------------------
write(
    "README.md",
    """# Healthcare ERP — Requirements Library

This library expands [`Healthcare-ERP-Pathway-and-Workflow.md`](../../Healthcare-ERP-Pathway-and-Workflow.md) into complete, implementable requirements for a **.NET 10 + React/TypeScript + PostgreSQL modular monolith**.

## Approved Delivery Baseline
| Decision | Choice |
|---|---|
| Requirements structure | One folder per major module + separate sub-module files |
| Stack | .NET 10 API, React/TypeScript SPA, PostgreSQL |
| Architecture | Modular monolith with domain events and strict module boundaries |
| Build style | Approval-gated increments |

## Requirement ID Convention
Format: `{MODULE}-{SUB}-TYPE-{NNN}`

| Segment | Meaning | Examples |
|---|---|---|
| MODULE | Major module | `FND`, `HMS`, `HRIS`, `FIN`, `INV`, `PRC`, `XWF` |
| SUB | Sub-module code | `PAT`, `OPD`, `GL`, `PO` |
| TYPE | Requirement type | `FR` functional, `BR` business rule, `AC` acceptance, `NFR` non-functional, `EVT` event |
| NNN | Zero-padded sequence | `001` |

## Module Map
| Folder | Module | Owns |
|---|---|---|
| [00-foundation](00-foundation/) | Integration hub & platform services | Tenancy, identity/RBAC, approvals engine, audit, notifications, documents, events, reporting contracts, data governance |
| [01-hms](01-hms/) | Hospital Management System | Patient master, encounters, clinical orders, diagnostics, pharmacy dispense (clinical), billing initiation, EMR |
| [02-hris](02-hris/) | Human Resource Information System | Employee master, credentials, roster, leave, payroll inputs, org hierarchy |
| [03-financials](03-financials/) | Financials | Chart of accounts, cost centers, GL, AP, AR, assets, cash/bank, tax, MIS |
| [04-inventory](04-inventory/) | Store & Spares | Item/SKU master, stores/bins, stock, batch/expiry, issues, transfers, counts |
| [05-procurement](05-procurement/) | Procurement | Vendor master, requisitions, RFQ, contracts, POs, vendor performance |
| [06-cross-module-workflows](06-cross-module-workflows/) | Cross-module pathways | End-to-end event choreography and reconciliation |

## Dependency Map
```mermaid
flowchart TB
  FND[Foundation Hub]
  HRIS[HRIS]
  FIN[Financials]
  INV[Inventory]
  PRC[Procurement]
  HMS[HMS]
  FND --> HRIS
  FND --> FIN
  FND --> INV
  FND --> PRC
  FND --> HMS
  HRIS --> HMS
  HRIS --> PRC
  HRIS --> FIN
  INV --> HMS
  INV --> PRC
  INV --> FIN
  PRC --> FIN
  PRC --> INV
  HMS --> FIN
  HMS --> INV
```

## Implementation Phasing (from blueprint §10)
1. **Phase 1 — Foundations**: master data, Foundation hub, core HMS (registration/OPD/billing), core Financials (GL/AP/AR).
2. **Phase 2 — Operations**: IPD, pharmacy, lab/radiology, Inventory, Procurement.
3. **Phase 3 — Workforce**: full HRIS integrated with HMS scheduling.
4. **Phase 4 — Optimization**: budgeting, analytics, portals, advanced MIS.

## Traceability Register
See [TRACEABILITY.md](TRACEABILITY.md) for requirement → design → code → test linkage.

## Verification Package
See [VERIFICATION.md](VERIFICATION.md) for consistency checks, file inventory, and open assumptions awaiting approval.

## Glossary
| Term | Definition |
|---|---|
| Integration hub | Shared Foundation services and master-data contracts used by all modules |
| Modular monolith | Single deployable solution with enforced module boundaries |
| Outbox/Inbox | Reliable messaging pattern for cross-module events |
| GRN | Goods Receipt Note |
| Three-way match | Matching PO, GRN, and vendor invoice before AP payment |
| FEFO | First-Expiry-First-Out stock issue rule |
| MAR | Medication Administration Record |
| TPA | Third-Party Administrator (insurance) |
| CME | Continuing Medical Education |
| Cost center | Financial responsibility unit (ward/department/equipment category) |
| Credential gate | HRIS check that blocks clinical actions when license/privilege is invalid |

## How to Review
1. Read this index and the Foundation overview first.
2. Review each module overview, then its sub-module files.
3. Review cross-module workflows.
4. Confirm or amend open assumptions in [VERIFICATION.md](VERIFICATION.md).
5. Approve the package before any application scaffolding begins.
""",
)


# ---------------------------------------------------------------------------
# Foundation
# ---------------------------------------------------------------------------
write(
    "00-foundation/00-module-overview.md",
    overview(
        "Foundation / Integration Hub",
        "FND",
        "Provides shared platform capabilities and master-data contracts so HMS, HRIS, Financials, Inventory, and Procurement never couple directly.",
        [
            ("Tenancy & Facilities", "01-tenancy-facilities.md", "Hospitals, sites, departments, wards"),
            ("Shared Master Data", "02-shared-master-data.md", "Cross-module identity of patient/employee/item/vendor/COA references"),
            ("Identity & RBAC", "03-identity-rbac.md", "Users, roles, permissions, session policy"),
            ("Approval Workflows", "04-approval-workflows.md", "Configurable approval engine"),
            ("Audit & Compliance", "05-audit-compliance.md", "Immutable audit trail and retention"),
            ("Notifications", "06-notifications.md", "In-app, email, SMS hooks"),
            ("Document Storage", "07-document-storage.md", "Secure document vault"),
            ("Integration Events", "08-integration-events.md", "Outbox/inbox event bus"),
            ("Reporting Contracts", "09-reporting.md", "Unified MIS/BI extract contracts"),
            ("Data Governance", "10-data-governance.md", "Privacy, retention, consent, residency"),
        ],
        [
            "Facility/tenant structure",
            "User identity and role model",
            "Approval workflow definitions",
            "Audit store",
            "Notification and document services",
            "Event infrastructure",
        ],
        [
            "Module-owned masters via reference IDs (patient, employee, item, vendor, COA)",
        ],
        "Phase 1 (must be first)",
        "Blueprint §§2, 9",
    ),
)

write(
    "00-foundation/01-tenancy-facilities.md",
    req_file(
        "Tenancy & Facilities",
        "FND",
        "TEN",
        "§1, §2, §9",
        "Support multi-department hospital or hospital group with sites, departments, wards, cost-center linkage, and facility-scoped configuration.",
        "Multi-tenant SaaS billing; franchise franchisee commercial management.",
        [
            "System Administrator — manage tenants/facilities",
            "Facility Admin — manage departments/wards for assigned facility",
            "All authenticated users — read authorized org structure",
        ],
        [
            "System shall support one or more facilities under an enterprise tenant.",
            "System shall model departments, wards, clinics, stores, and theatres as organizational units.",
            "Each organizational unit shall optionally map to a Financials cost center reference.",
            "Users and transactional data shall be scoped by facility unless enterprise role grants cross-facility access.",
            "Facility configuration shall allow enabling/disabling modules and sub-modules without schema breakage.",
            "Deactivated organizational units shall be retained for history and blocked from new assignments.",
        ],
        """```
Draft -> Active -> Inactive -> Archived
```
- Draft units are not selectable in operational transactions.
- Inactive units reject new links but keep historical references valid.""",
        [
            "`Tenant` — id, legal name, status",
            "`Facility` — id, tenantId, code, name, timezone, currency, status",
            "`OrgUnit` — id, facilityId, type(Department|Ward|Clinic|Store|Theatre|Other), parentId, costCenterRef?, status",
            "Validation: codes unique per parent; timezone IANA; currency ISO-4217",
        ],
        [
            "A user without cross-facility permission cannot read another facility's operational data.",
            "Cost center mapping is optional at create but required before financial postings from that unit.",
        ],
        "Creation/update of facilities requires System Administrator approval workflow when change-control mode is enabled; otherwise direct admin privilege.",
        [
            "POST /api/fnd/tenants",
            "GET/POST/PUT /api/fnd/facilities",
            "GET/POST/PUT /api/fnd/org-units",
        ],
        ["FacilityCreated", "OrgUnitChanged"],
        [],
        ["Notify Facility Admins on facility activation/deactivation"],
        ["Facility hierarchy listing", "Active units by type"],
        "All create/update/deactivate actions audited with actor, timestamp, before/after values. Retention per data-governance policy (default 7 years).",
        [
            "Optimistic concurrency via row version on Facility/OrgUnit.",
            "Idempotent create using client requestId.",
            "Reject orphan parent changes that would create cycles.",
        ],
        [
            "Org hierarchy read P95 < 200ms for 2,000 units.",
            "Support at least 50 facilities per tenant.",
        ],
        ["FND Identity/RBAC", "FIN cost center references (soft)"],
        [
            "Admin can create facility and nested department/ward structure.",
            "Inactive ward cannot be selected for new IPD admissions.",
            "Cost-center-linked unit is visible to Financials mapping APIs.",
        ],
        [
            "Initial deployment is single-tenant hospital group unless specified otherwise.",
            "Default currency and locale are configurable per facility.",
        ],
    ),
)

write(
    "00-foundation/02-shared-master-data.md",
    req_file(
        "Shared Master Data Contracts",
        "FND",
        "MDM",
        "§2",
        "Define canonical reference contracts and ownership rules for Patient, Employee, Item/SKU, Vendor, Chart of Accounts/Cost Centers, and Approval rules so modules share identity without duplicating masters.",
        "Full golden-record MDM UI beyond ownership/sync contracts in Phase 1.",
        [
            "Integration services — publish/consume master reference changes",
            "Module owners — authoritative CRUD in owning module",
            "Consuming modules — read-only projections/caches",
        ],
        [
            "Each master object shall have exactly one owning module as defined in the ownership table.",
            "Owning module shall publish create/update/deactivate events with stable global IDs.",
            "Consuming modules shall store only reference projections needed for local integrity and display.",
            "Hard deletes of master records are forbidden; only soft-deactivate/archive is allowed.",
            "Cross-module foreign keys shall reference global IDs, never local surrogate IDs of another module.",
            "Master change events shall be versioned and idempotent.",
        ],
        """Ownership:
| Object | Owner | Consumers |
|---|---|---|
| Patient | HMS | FIN, INV |
| Employee | HRIS | HMS, FIN, PRC, FND RBAC |
| Item/SKU | INV | HMS, PRC, FIN |
| Vendor | PRC | FIN, INV |
| COA / Cost Center | FIN | All |
| Approval rules | FND | All |

State for all masters: `Draft -> Active -> Suspended -> Archived`.""",
        [
            "`MasterReference` projection — globalId, ownerModule, type, code, displayName, status, version, lastSyncedAt",
            "Validation: globalId UUID; code non-empty; status enum enforced",
        ],
        [
            "Consumers must not mutate authoritative master attributes.",
            "If owner event version is older than local projection, ignore (idempotent).",
            "Suspended masters cannot be selected in new transactions.",
        ],
        "Master deactivation that impacts open transactions raises warning and may require approval depending on object type.",
        [
            "GET /api/fnd/master/{type}/{globalId}",
            "GET /api/fnd/master/{type}?query=",
            "POST /api/fnd/master/sync/replay (admin)",
        ],
        ["MasterProjectionUpdated"],
        [
            "PatientChanged (HMS)",
            "EmployeeChanged (HRIS)",
            "ItemChanged (INV)",
            "VendorChanged (PRC)",
            "AccountChanged / CostCenterChanged (FIN)",
        ],
        ["Admin alert on sync lag beyond threshold"],
        ["Master sync health", "Suspended masters in use"],
        "Projection sync operations audited. PHI/PII fields minimized in projections; full clinical data remains in HMS.",
        [
            "Exactly-once effective processing via inbox dedupe on eventId.",
            "Replay tool can rebuild projections from outbox archive.",
            "Concurrent consumer updates last-write by version number.",
        ],
        [
            "Projection update lag P95 < 5s under normal load.",
            "No cross-module direct DB joins in application code.",
        ],
        ["FND Integration Events", "Owning modules for each master"],
        [
            "Creating a patient in HMS makes patient selectable in billing/inventory projections.",
            "Suspended vendor cannot be used on new POs.",
            "Architecture tests fail if module references another module's persistence assembly.",
        ],
        [
            "Projections may cache display fields (name/code/status) only.",
            "National identifier formats are locale-configurable.",
        ],
    ),
)

write(
    "00-foundation/03-identity-rbac.md",
    req_file(
        "Identity & RBAC",
        "FND",
        "IAM",
        "§9 Governance — Role-based access control",
        "Single identity and role model governing access across HMS, HRIS, Financials, Inventory, and Procurement, sourced from HRIS employee linkage where applicable.",
        "External IdP federation beyond OIDC in Phase 1; advanced ABAC policies in Phase 4.",
        [
            "Security Admin — manage roles/permissions",
            "All users — authenticate and act within grants",
            "Service accounts — module-to-module internal calls",
        ],
        [
            "System shall authenticate users via secure token-based auth (OIDC-compatible).",
            "Every API authorization check shall evaluate role permissions and facility scope.",
            "Roles shall be composable permission sets assignable per facility.",
            "Employee-linked users shall inherit employment status gates from HRIS (active/exited).",
            "Privileged clinical actions shall optionally require credential checks via HRIS integration.",
            "Failed authorization attempts shall be logged without leaking sensitive resource details.",
            "Break-glass emergency access shall be supported with mandatory reason and heightened audit.",
        ],
        """User lifecycle: `Invited -> Active -> Locked -> Disabled`.
Role assignment: `PendingApproval(optional) -> Active -> Revoked`.""",
        [
            "`User`, `Role`, `Permission`, `UserRoleAssignment`, `FacilityScope`",
            "Permission codes namespaced by module, e.g. `HMS.Patient.Register`",
            "Password/secret storage never in application DB when external IdP used",
        ],
        [
            "Disabled/exited employees cannot authenticate except break-glass accounts.",
            "Permission checks are deny-by-default.",
            "A user may hold different roles in different facilities.",
        ],
        "Role creation and privileged role assignment require Security Admin approval workflow.",
        [
            "POST /api/fnd/auth/login (or external IdP)",
            "GET/POST /api/fnd/roles",
            "POST /api/fnd/users/{id}/roles",
            "GET /api/fnd/me",
        ],
        ["UserDisabled", "RoleAssignmentChanged"],
        ["EmployeeExited", "EmployeeCredentialStatusChanged"],
        ["Notify user on lockout", "Notify Security Admin on break-glass use"],
        ["Role matrix", "Access review report"],
        "Immutable security audit for login, logout, failures, role changes, break-glass. Retention minimum 7 years.",
        [
            "Token replay protection via jti/expiry.",
            "Concurrent role changes take effect on next authorization check.",
            "Idempotent role assignment APIs.",
        ],
        [
            "Authorization decision overhead P95 < 20ms cached.",
            "Support 5,000 concurrent authenticated users per deployment target.",
        ],
        ["FND Tenancy", "HRIS employee status/credentials", "FND Audit"],
        [
            "User without permission cannot access protected endpoint (403).",
            "Exited employee user is blocked at next request.",
            "Break-glass access is fully audited with reason.",
        ],
        [
            "Initial auth may use built-in Identity with migration path to external IdP.",
            "Permission catalog is code-defined and seeded.",
        ],
    ),
)

write(
    "00-foundation/04-approval-workflows.md",
    req_file(
        "Approval Workflow Engine",
        "FND",
        "APPR",
        "§9 Approval hierarchies; used by HRIS/Procurement/Financials",
        "Configurable approval hierarchies per transaction type and value threshold, reusable across leave/hiring, purchase orders, and payment release.",
        "Document-centric BPM suite; free-form process designer beyond structured steps.",
        [
            "Workflow Admin — define templates",
            "Approvers — approve/reject/escalate",
            "Requestors — submit and track",
        ],
        [
            "System shall allow defining approval templates by transaction type, facility, and amount/value rules.",
            "Approval routing shall resolve approvers from HRIS org hierarchy and explicit role maps.",
            "Requests shall support approve, reject, request-info, and escalate actions.",
            "Parallel and sequential steps shall be supported.",
            "SLA timers shall escalate overdue approvals.",
            "Modules shall start approvals via a common API and receive decision events.",
        ],
        """```
Draft -> Submitted -> InApproval -> Approved | Rejected | Cancelled
InApproval -> Escalated -> InApproval
```""",
        [
            "`ApprovalTemplate`, `ApprovalStep`, `ApprovalRequest`, `ApprovalAction`",
            "Value rules: min/max amount, currency, cost center",
            "Validation: at least one step; no unresolved approver group at runtime start",
        ],
        [
            "Requestor cannot approve their own request unless policy explicitly allows.",
            "Rejected requests are immutable except cancellation/archive.",
            "Template changes do not alter in-flight requests.",
        ],
        "Self-governing: template publish may itself require approval for sensitive transaction types.",
        [
            "POST /api/fnd/approvals/templates",
            "POST /api/fnd/approvals/requests",
            "POST /api/fnd/approvals/requests/{id}/actions",
            "GET /api/fnd/approvals/inbox",
        ],
        ["ApprovalRequested", "ApprovalDecisionMade", "ApprovalEscalated"],
        ["EmployeeOrgChanged (HRIS) for routing refresh on new requests"],
        ["Approver inbox notification", "Escalation notification", "Final decision to requestor"],
        ["Pending approvals aging", "Approval cycle-time by type"],
        "Every action immutable with comment, actor, timestamp. Approval artifacts retained with related business transaction retention.",
        [
            "Action APIs idempotent by actionRequestId.",
            "Concurrent approve/reject: first commit wins; second gets conflict.",
            "Missing approver resolution fails request start with clear error.",
        ],
        [
            "Start approval P95 < 300ms.",
            "Support 10,000 open approval requests.",
        ],
        ["FND IAM", "HRIS org hierarchy", "FND Notifications"],
        [
            "PO above threshold routes to correct approver chain.",
            "Overdue step escalates per template SLA.",
            "Decision event is consumed by originating module to advance state.",
        ],
        [
            "Amount thresholds are in facility base currency unless multi-currency rules configured.",
            "Delegation/out-of-office can be Phase 2 enhancement if not in MVP.",
        ],
    ),
)

write(
    "00-foundation/05-audit-compliance.md",
    req_file(
        "Audit & Compliance Trail",
        "FND",
        "AUD",
        "§9 Audit trail",
        "Provide immutable, timestamped, user-tagged audit records for every regulated transaction across all modules.",
        "External SIEM product integration beyond export APIs in Phase 1.",
        [
            "Compliance Officer — search/export audits",
            "All modules — write audit records via shared SDK",
            "Security Admin — configure retention categories",
        ],
        [
            "Every state-changing business operation shall write an audit record.",
            "Audit records shall include actor, facility, correlationId, entity type/id, action, before/after (or diff), timestamp (UTC), and source module.",
            "Audit records shall be append-only; updates/deletes are not permitted via application APIs.",
            "System shall support filtered search and legal export.",
            "High-sensitivity entities (drug dispense, financial postings, credential overrides) shall be marked with compliance category tags.",
        ],
        """Audit records have no editable lifecycle; operational index states: `Writable(hot) -> Warm -> ArchivedCold` for storage tiering only.""",
        [
            "`AuditEvent` — immutable",
            "Optional `AuditExportJob`",
            "PII in audit payloads minimized/redacted per policy",
        ],
        [
            "Application modules cannot bypass audit SDK for marked command types.",
            "Clock skew tolerance recorded; server UTC is authoritative.",
        ],
        "Retention policy changes require Compliance Officer approval.",
        [
            "GET /api/fnd/audit",
            "POST /api/fnd/audit/exports",
            "GET /api/fnd/audit/exports/{id}",
        ],
        ["AuditExportCompleted"],
        [],
        ["Notify requester when export ready"],
        ["Audit activity by module", "Sensitive action report"],
        "Audit store is the compliance system of record. Default retention 7–10 years configurable by category. Patient-identifiable audit access is itself audited.",
        [
            "Audit write failures fail the business transaction or enqueue guaranteed write per policy (at-least-once with dedupe key).",
            "Export jobs restartable/idempotent.",
        ],
        [
            "Audit write overhead budgeted < 15ms P95 amortized.",
            "Search over 90 days hot data P95 < 2s for common filters.",
        ],
        ["FND IAM", "FND Data Governance"],
        [
            "Creating a clinical order produces an audit record with actor and entity ids.",
            "Attempt to update audit record via API is rejected.",
            "Export contains expected filtered subset.",
        ],
        [
            "Exact regulatory regime (HIPAA/GDPR/local) selected per deployment configuration.",
        ],
    ),
)

write(
    "00-foundation/06-notifications.md",
    req_file(
        "Notifications",
        "FND",
        "NTF",
        "§9; alerts across modules (credential expiry, reorder, approvals, variance)",
        "Central notification dispatch for in-app, email, and pluggable SMS/push providers.",
        "Marketing campaigns; patient engagement CRM.",
        [
            "All users — receive in-app notifications",
            "Notification Admin — templates and channel settings",
            "Modules — raise notification requests",
        ],
        [
            "Modules shall raise notifications through a shared API/event with template key and data payload.",
            "Users shall manage channel preferences within policy constraints (some compliance notices mandatory).",
            "System shall support delivery status tracking and retries for external channels.",
            "In-app notifications shall support read/unread state.",
            "Template rendering shall prevent XSS and avoid leaking unauthorized PHI fields.",
        ],
        """Notification: `Queued -> Sending -> Sent | Failed -> DeadLetter`.
In-app message: `Unread -> Read -> Archived`.""",
        [
            "`NotificationTemplate`, `NotificationMessage`, `DeliveryAttempt`, `UserNotificationPreference`",
        ],
        [
            "Mandatory compliance templates ignore user opt-out for that channel if legally required.",
            "Payload fields are allow-listed per template.",
        ],
        "Template publish for patient-facing content may require approval.",
        [
            "POST /api/fnd/notifications",
            "GET /api/fnd/notifications/me",
            "POST /api/fnd/notifications/me/{id}/read",
            "PUT /api/fnd/notifications/preferences",
        ],
        ["NotificationDispatched", "NotificationFailed"],
        ["Any module domain alert events"],
        ["Channel delivery itself"],
        ["Delivery failure rates", "Unread counts"],
        "Notification content that includes PHI follows same retention/access controls as source module; prefer deep links over embedding PHI.",
        [
            "Publish API idempotent by notificationRequestId.",
            "Retry with exponential backoff; poison messages to dead letter.",
        ],
        [
            "In-app fanout P95 < 2s.",
            "Email provider timeouts do not block core transactions.",
        ],
        ["FND IAM", "FND Events"],
        [
            "Approval request creates in-app notification for approver.",
            "Failed email is retried and visible in dead-letter admin view.",
        ],
        [
            "SMS/push providers are optional integrations.",
        ],
    ),
)

write(
    "00-foundation/07-document-storage.md",
    req_file(
        "Document Storage",
        "FND",
        "DOC",
        "§4 HRIS documents/licenses; clinical attachments; vendor certificates",
        "Secure document vault for licenses, clinical attachments, vendor certificates, and financial artifacts with virus-scan hook and access control.",
        "Full DAM/PACS image archive (RIS/PACS owns imaging binaries/integration).",
        [
            "All authorized users — upload/download per ACL",
            "Document Admin — retention classes and quotas",
        ],
        [
            "Documents shall be stored encrypted at rest with module/entity linkage metadata.",
            "Access shall require permission on the owning business entity.",
            "Uploads shall enforce type/size limits and optional malware scan gate.",
            "Versioning shall be supported for replaceable documents (e.g., renewed license).",
            "Deletion shall be soft-delete/legal-hold aware.",
        ],
        """`Uploading -> Quarantined -> Available -> Superseded -> Deleted(soft)`.
Legal hold blocks delete.""",
        [
            "`DocumentObject`, `DocumentVersion`, `DocumentLink(entityType, entityId)`, `LegalHold`",
        ],
        [
            "Download URLs are short-lived and scoped.",
            "Clinical documents inherit patient access rules from HMS.",
        ],
        "Bulk purge requires Compliance approval.",
        [
            "POST /api/fnd/documents (multipart or signed upload)",
            "GET /api/fnd/documents/{id}",
            "GET /api/fnd/documents/{id}/content",
            "POST /api/fnd/documents/{id}/versions",
        ],
        ["DocumentAvailable", "DocumentSuperseded"],
        [],
        ["Scan failure notice to uploader"],
        ["Storage usage by module", "Expiring linked credentials documents"],
        "Documents classified by sensitivity. Retention tied to entity class. Access audited.",
        [
            "Upload initiation idempotent by uploadSessionId.",
            "Concurrent version upload creates distinct versions with monotonic numbers.",
        ],
        [
            "Support files up to configurable max (default 25MB non-DICOM).",
            "Signed download URL TTL default 5 minutes.",
        ],
        ["FND IAM", "FND Audit", "Object storage provider"],
        [
            "Uploading employee license makes document retrievable only to authorized HR/credential roles.",
            "Quarantined file is not downloadable by standard users.",
        ],
        [
            "Object storage is S3-compatible or local emulator for development.",
        ],
    ),
)

write(
    "00-foundation/08-integration-events.md",
    req_file(
        "Integration Events (Outbox/Inbox)",
        "FND",
        "EVT",
        "§2 Integration hub; all module integration triggers",
        "Reliable asynchronous integration between modules using transactional outbox and inbox deduplication, schema-versioned event contracts.",
        "External enterprise service bus products; public webhook marketplace in Phase 1.",
        [
            "Platform engineers — monitor bus health",
            "All modules — publish/consume via shared abstractions",
        ],
        [
            "State-changing use cases that require cross-module effects shall publish integration events in the same DB transaction as the write (outbox pattern).",
            "Consumers shall process events idempotently via inbox dedupe keys.",
            "Event contracts shall be versioned (v1, v2) and backward compatible within major version.",
            "Failed handlers shall retry with backoff and then dead-letter with alerting.",
            "Ordering shall be guaranteed per aggregate partition key where required (e.g., stock item).",
            "There shall be an admin replay capability for selected event types.",
        ],
        """Outbox: `Pending -> Dispatched -> Completed | Failed`.
Inbox: `Received -> Processed | DeadLetter`.""",
        [
            "`OutboxMessage`, `InboxMessage`, `DeadLetterMessage`, `EventSchemaRegistry` entry",
            "Envelope: eventId, eventType, occurredAt, correlationId, causationId, partitionKey, payload, version",
        ],
        [
            "No module may call another module's internal repositories.",
            "Sync query APIs are allowed for reads; writes across modules go through events or explicit application services at the host composition root only when strongly consistent and documented.",
        ],
        "Replay of financial/clinical events may require Compliance/Finance approval in production.",
        [
            "GET /api/fnd/events/outbox/health",
            "GET /api/fnd/events/dead-letters",
            "POST /api/fnd/events/dead-letters/{id}/replay",
        ],
        ["EventDeadLetterCreated"],
        [],
        ["Alert ops on dead-letter threshold"],
        ["Event throughput", "Dead-letter aging", "Consumer lag"],
        "Event payloads avoid unnecessary PHI; use references. Event archives follow retention policy.",
        [
            "Publisher uses transaction + outbox.",
            "Consumer idempotent by eventId.",
            "Poison message isolation after N attempts.",
        ],
        [
            "At-least-once delivery semantics.",
            "Dispatch lag P95 < 5s normal load.",
        ],
        ["PostgreSQL", "All modules"],
        [
            "Stock issue publishes event and inventory write atomically.",
            "Duplicate delivery does not double-post financial entries.",
            "Architecture tests enforce module boundary rules.",
        ],
        [
            "In-process dispatcher is acceptable for modular monolith MVP; can swap to broker later.",
        ],
    ),
)

write(
    "00-foundation/09-reporting.md",
    req_file(
        "Reporting & Analytics Contracts",
        "FND",
        "RPT",
        "§9 Reporting & analytics; cost-per-patient, profitability, turnover, staff cost, vendor performance",
        "Unified MIS/BI layer contracts and operational report APIs pulling from all modules without breaking ownership boundaries.",
        "Full custom pixel-perfect report designer in Phase 1; advanced AI analytics in Phase 4.",
        [
            "Executives / Department heads — consume dashboards",
            "Report Admin — publish report definitions",
            "Modules — provide read models / export facts",
        ],
        [
            "Each module shall publish analytical fact/projection contracts for approved metrics.",
            "Foundation shall provide a report catalog and parameterized execution API.",
            "Dashboards shall enforce the same RBAC and facility scoping as operational data.",
            "Standard KPI set shall include cost-per-patient, department profitability, inventory turnover, staff cost ratio, and vendor performance.",
            "Exports shall be auditable.",
        ],
        """ReportDefinition: `Draft -> Published -> Retired`.
ReportRun: `Queued -> Running -> Succeeded | Failed`.""",
        [
            "`ReportDefinition`, `ReportRun`, semantic KPI identifiers",
            "Fact tables/projections owned per module, cataloged centrally",
        ],
        [
            "Reports cannot bypass row-level facility security.",
            "Heavy reports run asynchronously.",
        ],
        "Publishing enterprise-wide financial reports may require Finance Controller approval.",
        [
            "GET /api/fnd/reports",
            "POST /api/fnd/reports/{key}/runs",
            "GET /api/fnd/reports/runs/{id}",
            "GET /api/fnd/kpis/{key}",
        ],
        ["ReportRunCompleted"],
        ["Module fact projection updates"],
        ["Report completion notice"],
        ["All catalog reports listed in module files"],
        "Report access and exports audited. Aggregates preferred over row-level PHI.",
        [
            "Report runs idempotent by runRequestId.",
            "Timeouts mark Failed with retry option.",
        ],
        [
            "Interactive KPI cards P95 < 2s on warmed aggregates.",
            "Async large export within configured SLA.",
        ],
        ["All modules' reporting projections", "FND IAM"],
        [
            "Authorized user can run department profitability for their facility.",
            "Unauthorized cross-facility report is denied.",
        ],
        [
            "Initial implementation may use SQL views/read models; OLAP warehouse optional later.",
        ],
    ),
)

write(
    "00-foundation/10-data-governance.md",
    req_file(
        "Data Governance, Privacy & Retention",
        "FND",
        "GOV",
        "§9 Regulatory & compliance",
        "Enterprise policies for privacy, consent, retention, legal hold, and data residency covering clinical, HR, financial, and vendor data.",
        "External DLP product replacement; patient portal consent UX details belong partly to HMS portals.",
        [
            "Compliance Officer — policies",
            "Data Protection Officer — privacy requests",
            "Module owners — implement classification",
        ],
        [
            "All personal data entities shall declare sensitivity classification.",
            "Retention schedules shall be configurable by data class and jurisdiction.",
            "Legal hold shall suspend purge.",
            "Subject access / export / rectification workflows shall be supported with module participation.",
            "Production data shall not be copied to non-prod without anonymization controls.",
        ],
        """Policy: `Draft -> Active -> Retired`.
PrivacyRequest: `Received -> InProgress -> Completed | Rejected`.""",
        [
            "`DataClass`, `RetentionPolicy`, `LegalHold`, `PrivacyRequest`",
        ],
        [
            "Clinical data retention overrides generic defaults when stricter.",
            "Financial postings are never physically deleted within statutory period.",
        ],
        "Activation of retention policy changes requires Compliance approval.",
        [
            "GET/POST /api/fnd/governance/policies",
            "POST /api/fnd/governance/privacy-requests",
            "POST /api/fnd/governance/legal-holds",
        ],
        ["PrivacyRequestCompleted", "LegalHoldApplied"],
        [],
        ["DPO notified on new privacy request"],
        ["Retention upcoming purges", "Privacy request SLA"],
        "Governance configuration changes fully audited. Privacy request handling audited end-to-end.",
        [
            "Purge jobs are dry-run capable and idempotent.",
            "Holds always win over purge.",
        ],
        [
            "Policy evaluation available synchronously for delete operations.",
        ],
        ["FND Audit", "All modules"],
        [
            "Record under legal hold cannot be purged.",
            "Privacy export includes data from participating modules for a subject.",
        ],
        [
            "Jurisdiction pack (e.g., PK/US/EU) selected at deployment.",
        ],
    ),
)

print("Foundation written")


# ---------------------------------------------------------------------------
# HMS
# ---------------------------------------------------------------------------
write(
    "01-hms/00-module-overview.md",
    overview(
        "Hospital Management System (HMS)",
        "HMS",
        "Manage the patient clinical and administrative pathway from registration through discharge and follow-up, integrating with Inventory, Financials, and HRIS credential gates.",
        [
            ("Front Office", "01-front-office.md", "Appointments, registration, insurance/TPA verification"),
            ("OPD", "02-opd.md", "Outpatient encounters and consultation"),
            ("IPD / Bed / Nursing", "03-ipd-bed-nursing.md", "Admission, beds, nursing, MAR, consumables"),
            ("Emergency & Triage", "04-emergency-triage.md", "Triage routing and emergency care"),
            ("Operation Theatre", "05-ot.md", "OT scheduling, checklists, implant/consumable usage"),
            ("Laboratory (LIS)", "06-lis.md", "Lab orders, samples, results"),
            ("Radiology / RIS-PACS", "07-ris-pacs.md", "Imaging orders, reports, PACS link"),
            ("Pharmacy", "08-pharmacy.md", "Inpatient and retail dispense"),
            ("Medical Records (EMR/EHR)", "09-emr-ehr.md", "Clinical documentation and orders"),
            ("Billing & Claims", "10-billing-claims.md", "Charges, bills, insurance claims"),
            ("Discharge & Follow-up", "11-discharge-follow-up.md", "Discharge summary, follow-up, portal handoff"),
        ],
        ["Patient master", "Encounters", "Clinical orders", "EMR documents", "Bills/claims (originating)"],
        ["Employee/credentials (HRIS)", "Item stock availability (INV)", "COA/cost centers (FIN)", "Approvals/RBAC (FND)"],
        "Phase 1 core (registration/OPD/billing); Phase 2 operational sub-modules",
        "Blueprint §3",
    ),
)

HMS_SUBS = [
    (
        "01-front-office.md",
        "Front Office — Registration, Appointments, Insurance/TPA",
        "FO",
        "§3.1 Front office; §3.2 steps 1,9",
        "Patient registration (new/returning), appointment scheduling, and insurance/TPA eligibility verification.",
        "Full insurer adjudication engine (claims belong with billing); CRM marketing.",
        [
            "Front Desk Officer",
            "Insurance Desk",
            "Patient (portal booking — Phase 4)",
            "Scheduling Supervisor",
        ],
        [
            "Register new patients into patient master with demographics and identifiers.",
            "Match returning patients to avoid duplicates using configurable match rules.",
            "Schedule, reschedule, and cancel appointments against providers and clinics.",
            "Verify insurance/TPA eligibility and capture coverage snapshot for the visit.",
            "Capture referral source and visit reason.",
            "Support walk-in queue tickets linked to OPD/Emergency routing.",
        ],
        """Patient: `Active | Merged | Inactive`.
Appointment: `Scheduled -> CheckedIn -> InProgress -> Completed | Cancelled | NoShow`.
Eligibility check: `NotChecked -> Verified | Pending | Failed`.""",
        [
            "`Patient`, `PatientIdentifier`, `Appointment`, `InsurancePolicy`, `EligibilityCheck`",
            "Validation: names required; DOB; at least one phone/ID per facility policy; appointment slot conflicts prevented per provider",
        ],
        [
            "Duplicate patients are merged via controlled merge with audit, not hard-deleted.",
            "Appointment with clinician requires clinician active + credential OK from HRIS gate.",
            "Eligibility failure can soft-block or warn based on facility policy.",
        ],
        "Patient merge and large appointment template changes may require supervisor approval.",
        [
            "POST /api/hms/patients",
            "GET /api/hms/patients/{id}",
            "POST /api/hms/appointments",
            "POST /api/hms/insurance/eligibility-checks",
        ],
        ["PatientChanged", "AppointmentScheduled", "AppointmentCheckedIn", "EligibilityVerified"],
        ["EmployeeCredentialStatusChanged"],
        ["Appointment reminders", "Eligibility failure to insurance desk"],
        ["Daily appointment list", "Registration volume", "Insurance verification turnaround"],
        "Patient demographics are PHI. Access audited. Retention per clinical records policy.",
        [
            "Registration API idempotent by requestId.",
            "Double-booking prevented with transactional slot lock.",
        ],
        ["Search patient P95 < 300ms", "Support high front-desk concurrency at opening hours"],
        ["FND IAM/Tenancy", "HRIS credentials for provider scheduling", "FIN payer refs optional"],
        [
            "New patient registration creates selectable patient master record.",
            "Cannot schedule inactive/unlicensed clinician.",
            "Checked-in appointment is available to OPD worklist.",
        ],
        ["Default ID types configurable (CNIC/MRN/passport/etc.)."],
    ),
    (
        "02-opd.md",
        "Outpatient Department (OPD)",
        "OPD",
        "§3.1 OPD; §3.2 steps 2–4",
        "Manage outpatient consultation encounters, vitals, clinical notes handoff to EMR, and order placement.",
        "Full inpatient nursing; long-stay billing specifics.",
        ["OPD Physician", "OPD Nurse", "OPD Clerk"],
        [
            "Create OPD encounter from checked-in appointment or walk-in.",
            "Record vitals and chief complaint.",
            "Allow clinician to document assessment/plan via EMR integration.",
            "Place lab/radiology/medication/procedure orders from encounter.",
            "Close encounter with disposition (home, admit, refer ER, follow-up).",
            "Post consultation charges to billing.",
        ],
        """Encounter: `Open -> InConsultation -> AwaitingOrders -> Closed | Cancelled`.
Disposition recorded on close.""",
        [
            "`OpdEncounter`, `VitalSigns`, link to `ClinicalOrder`s and EMR note ids",
        ],
        [
            "Only credentialed clinicians can sign consultation notes/orders.",
            "Closing encounter with unsigned mandatory notes blocked if policy requires.",
            "Admit disposition starts IPD admission workflow.",
        ],
        "Encounter cancellation after charges may require billing supervisor approval.",
        [
            "POST /api/hms/opd/encounters",
            "POST /api/hms/opd/encounters/{id}/vitals",
            "POST /api/hms/opd/encounters/{id}/close",
        ],
        ["OpdEncounterOpened", "OpdEncounterClosed", "ClinicalOrderPlaced"],
        ["LabResultPosted", "RadiologyReportPosted", "MedicationDispensed"],
        ["Nurse alert for pending vitals", "Physician alert for critical results"],
        ["OPD volume by clinic", "Average consultation time"],
        "Clinical documentation PHI; signed note amendments audited.",
        ["Concurrent note edits use optimistic concurrency", "Order place idempotent"],
        ["Worklist refresh under 2s"],
        ["HMS Front Office", "HMS EMR", "HRIS credentials", "FIN billing events"],
        [
            "Checked-in patient appears on physician worklist.",
            "Signed order creates fulfillment workitem in LIS/RIS/Pharmacy.",
            "Consultation fee appears on patient bill.",
        ],
        ["OPD charge master codes maintained in billing configuration."],
    ),
    (
        "03-ipd-bed-nursing.md",
        "IPD / Bed Management / Nursing",
        "IPD",
        "§3.1 IPD; §3.2 steps 5",
        "Admissions, bed allocation, nursing care plans, daily MAR, and per-bed consumable tracking.",
        "Home-care episodes; external referral hospital bed network.",
        ["Admission Desk", "Ward Nurse", "Nursing Supervisor", "Attending Physician", "Bed Management"],
        [
            "Admit patient to IPD with admitting diagnosis and attending clinician.",
            "Allocate/transfer beds with occupancy integrity.",
            "Maintain nursing care plan and shift handover notes.",
            "Record medication administration (MAR) against pharmacy-dispensed orders.",
            "Track consumables issued to patient/bed and post usage.",
            "Capture daily ward charges automatically based on bed class.",
        ],
        """Admission: `Requested -> Admitted -> Transferred -> DischargeInitiated -> Discharged`.
Bed: `Available -> Occupied -> Blocked -> Maintenance`.
MAR dose: `Due -> Administered | Held | Refused | Missed`.""",
        [
            "`Admission`, `Bed`, `BedAssignment`, `NursingCarePlan`, `MarEntry`, `PatientConsumableUsage`",
        ],
        [
            "Bed cannot be double-occupied.",
            "MAR administration requires active nursing credential/role.",
            "Consumable issue decrements inventory via events and charges bill.",
        ],
        "Bed block beyond duration and backdated admission corrections require supervisor approval.",
        [
            "POST /api/hms/ipd/admissions",
            "POST /api/hms/ipd/beds/{id}/assign",
            "POST /api/hms/ipd/mar",
            "POST /api/hms/ipd/consumables",
        ],
        ["PatientAdmitted", "BedAssignmentChanged", "MarAdministered", "ConsumableUsed"],
        ["MedicationDispensed", "StockAvailabilityChanged", "EmployeeCredentialStatusChanged"],
        ["Bed occupancy alerts", "Overdue MAR alerts"],
        ["Bed occupancy", "Average length of stay", "MAR compliance"],
        "IPD clinical and admin events audited; medication admin records immutable after sign with amendment trail.",
        ["Bed assignment transactional lock", "MAR entry idempotent by doseInstanceId"],
        ["Occupancy board near-real-time (<5s)"],
        ["HMS Pharmacy/EMR/Billing", "INV stock", "HRIS credentials", "FIN charges"],
        [
            "Admission allocates available bed and starts room rent accrual.",
            "Administered MAR dose cannot be silently deleted.",
            "Consumable usage reduces ward store stock.",
        ],
        ["Bed classes map to charge items in billing."],
    ),
    (
        "04-emergency-triage.md",
        "Emergency & Triage",
        "ER",
        "§3.1 Emergency; §3.2 step 2",
        "Triage assessment, emergency encounter management, and routing to OPD/IPD/OT as needed.",
        "Ambulance fleet management; disaster external command systems.",
        ["Triage Nurse", "ER Physician", "ER Clerk"],
        [
            "Register/identify emergency patient rapidly (including unidentified patient workflow).",
            "Capture triage score/category and vitals.",
            "Track ER encounter timeline and interventions.",
            "Route to admission, OT, or discharge from ER.",
            "Support emergency override for credential/payment soft-blocks with audit.",
        ],
        """Triage: `Arrived -> Triaged -> InTreatment -> Disposed`.
Disposition: `Discharge | AdmitIPD | Transfer | Deceased | LAMA`.""",
        ["`ErEncounter`", "`TriageAssessment`", "unidentified patient temporary IDs"],
        [
            "Critical triage category gets queue prioritization.",
            "Unidentified patients can receive orders; identity merge later.",
        ],
        "Emergency break-glass clinical access uses FND IAM break-glass with reason.",
        [
            "POST /api/hms/er/encounters",
            "POST /api/hms/er/encounters/{id}/triage",
            "POST /api/hms/er/encounters/{id}/dispose",
        ],
        ["ErEncounterOpened", "PatientTriaged", "ErDisposed"],
        ["EmployeeCredentialStatusChanged"],
        ["Critical triage alerts to ER team"],
        ["ER wait times", "Triage category mix"],
        "ER records PHI; high audit scrutiny on overrides.",
        ["Unidentified ID generation unique", "Disposition idempotent"],
        ["Triage board real-time updates"],
        ["HMS Front Office/IPD/OT/Billing", "FND IAM"],
        [
            "Unidentified patient can be created in <60 seconds path.",
            "Admit disposition creates IPD admission request.",
        ],
        ["Triage scale configurable (e.g., ESI/local)."],
    ),
    (
        "05-ot.md",
        "Operation Theatre Scheduling & Management",
        "OT",
        "§3.1 OT; §3.2 step 6",
        "Theatre scheduling, pre-op checklist, intra-op documentation hooks, and implant/consumable usage logging against patient.",
        "Full anesthesia information system depth in later phases; robotic device telemetry.",
        ["OT Scheduler", "Surgeon", "Anesthetist", "OT Nurse"],
        [
            "Schedule OT cases with theatre, team, and equipment requirements.",
            "Enforce pre-op checklist completion before start.",
            "Record procedure start/end and team timeouts.",
            "Log implants/consumables used and send to Inventory + Billing.",
            "Capture post-op destination (recovery/ICU/ward).",
        ],
        """OT Case: `Requested -> Scheduled -> PreOp -> InProgress -> Completed | Cancelled`.
Checklist: `Pending -> Completed`.""",
        ["`OtCase`", "`OtChecklist`", "`OtImplantUsage`", "`OtTeamAssignment`"],
        [
            "Surgeon/anesthetist must have valid specialty privileges.",
            "Implant usage requires batch/serial capture for traceable items.",
            "Overlapping exclusive theatre bookings forbidden.",
        ],
        "Case cancellation after consumable reservation may require supervisor approval.",
        [
            "POST /api/hms/ot/cases",
            "POST /api/hms/ot/cases/{id}/checklist",
            "POST /api/hms/ot/cases/{id}/usage",
            "POST /api/hms/ot/cases/{id}/complete",
        ],
        ["OtCaseScheduled", "OtCaseCompleted", "OtImplantUsed"],
        ["StockAvailabilityChanged", "EmployeeCredentialStatusChanged"],
        ["Schedule changes to OT team", "Missing checklist blockers"],
        ["OT utilization", "Case cancellation reasons", "Implant usage register"],
        "Surgical records and implant registers retained per clinical device regulations; immutable usage log.",
        ["Theatre schedule conflict detection transactional", "Usage posting idempotent"],
        ["Schedule board consistent across concurrent editors"],
        ["HMS IPD/EMR/Billing", "INV stock", "HRIS privileges", "FIN charges/assets optional"],
        [
            "Completing OT case with implants decrements stock and adds bill charges.",
            "Case cannot start with incomplete mandatory checklist.",
        ],
        ["Checklist templates configurable per procedure type."],
    ),
    (
        "06-lis.md",
        "Laboratory Information System (LIS)",
        "LIS",
        "§3.1 LIS; §3.2 order fulfillment labs",
        "Lab order intake, sample collection, processing, result entry/validation, and auto-post to EMR.",
        "Full analyzer middleware device drivers beyond generic interface adapter; external reference lab network portal.",
        ["Phlebotomist", "Lab Technologist", "Pathologist", "Ordering Clinician (read)"],
        [
            "Receive clinical lab orders from EMR/OPD/IPD/ER.",
            "Generate sample collection lists and capture sample IDs.",
            "Track sample lifecycle and rejects/recollects.",
            "Enter/import results and support clinical validation/sign-out.",
            "Auto-post finalized results to EMR and notify ordering clinician.",
            "Post diagnostic charges on order accept/complete per billing rules.",
        ],
        """Order: `Received -> Collected -> InProcess -> Preliminary -> Final | Cancelled`.
Sample: `Collected -> Accepted | Rejected`.""",
        ["`LabOrder`", "`LabSample`", "`LabResult`", "`Analyte` master refs"],
        [
            "Final result requires authorized validator role.",
            "Critical values trigger mandatory notification.",
            "Amended results create new version linked to prior final.",
        ],
        "Manual charge write-off for cancelled lab after resulting requires billing approval.",
        [
            "POST /api/hms/lis/orders/accept",
            "POST /api/hms/lis/samples",
            "POST /api/hms/lis/results",
            "POST /api/hms/lis/results/{id}/finalize",
        ],
        ["LabOrderAccepted", "LabResultPosted", "CriticalValueAlert"],
        ["ClinicalOrderPlaced"],
        ["Critical value alerts", "Recollect requests"],
        ["TAT by test", "Critical value log", "Workload"],
        "Lab results are clinical records; amendments audited; retention per lab regulations.",
        ["Result finalize idempotent", "Sample ID unique per facility"],
        ["Result post to EMR lag P95 < 5s"],
        ["HMS EMR/Billing", "FND Notifications"],
        [
            "Finalized result appears in patient EMR.",
            "Critical result notifies ordering clinician.",
        ],
        ["Device integration adapters phased after core LIS."],
    ),
    (
        "07-ris-pacs.md",
        "Radiology / RIS / PACS Integration",
        "RIS",
        "§3.1 Radiology/PACS; §3.2 imaging fulfillment",
        "Imaging order management, scheduling, report creation, and PACS study linkage with auto-post to EMR.",
        "Replacing vendor PACS; advanced 3D workstation.",
        ["Radiographer", "Radiologist", "RIS Clerk", "Ordering Clinician"],
        [
            "Accept radiology orders and schedule modalities.",
            "Track study acquisition status and PACS accession/study UIDs.",
            "Create/sign radiology reports.",
            "Auto-post signed reports to EMR.",
            "Post imaging charges per protocol.",
        ],
        """Study: `Ordered -> Scheduled -> Acquired -> Reporting -> Reported | Cancelled`.""",
        ["`RadiologyOrder`", "`ImagingStudy`", "`RadiologyReport`", "PACS identifiers"],
        [
            "Only radiologist role can finalize diagnostic report.",
            "Report amendments versioned.",
            "PACS link optional for MVP with manual acquisition confirmation.",
        ],
        "After-hours report privilege overrides audited.",
        [
            "POST /api/hms/ris/orders/accept",
            "POST /api/hms/ris/studies/{id}/acquire",
            "POST /api/hms/ris/reports",
            "POST /api/hms/ris/reports/{id}/sign",
        ],
        ["RadiologyOrderAccepted", "RadiologyReportPosted"],
        ["ClinicalOrderPlaced"],
        ["STAT study alerts", "Unsigned report aging"],
        ["Modality utilization", "Report TAT"],
        "Imaging reports clinical PHI; PACS URLs access-controlled; audit downloads/views of reports.",
        ["Sign report idempotent", "Accession uniqueness"],
        ["Report availability in EMR < 5s after sign"],
        ["HMS EMR/Billing", "External PACS optional"],
        [
            "Signed report visible in EMR.",
            "STAT order prioritized on worklist.",
        ],
        ["DICOM integration can be adapter-based in Phase 2+."],
    ),
    (
        "08-pharmacy.md",
        "Pharmacy (In-patient and Retail)",
        "PHX",
        "§3.1 Pharmacy; §3.2 medication fulfillment; §3.3 dispense -> inventory",
        "Medication order verification, dispensing from Inventory stock, patient counseling/retail sales, and charge posting.",
        "Robotics/cabinet device control; full clinical decision support beyond basic interactions in MVP.",
        ["Pharmacist", "Pharmacy Technician", "Retail Cashier", "Ordering Clinician"],
        [
            "Receive medication orders and perform pharmacist verification.",
            "Allocate batches via FEFO from configured pharmacy stores.",
            "Dispense inpatient and retail prescriptions with labeling data.",
            "Decrement Inventory stock through integration events/commands.",
            "Auto-post medication charges to patient bill / retail receipt.",
            "Support returns/wastage with reason codes.",
        ],
        """Med order pharmacy state: `New -> Verified -> PartiallyDispensed -> Dispensed | Rejected | Cancelled`.
Dispense: `Posted` immutable except return document.""",
        ["`MedicationOrder`", "`DispenseTransaction`", "`DispenseLine(batch)`", "`PharmacyReturn`"],
        [
            "Cannot dispense more than ordered without amendment.",
            "Expired batches cannot be dispensed.",
            "Credentialed pharmacist required for verification where policy mandates.",
            "Below-reorder resulting stock triggers procurement requisition via Inventory rules.",
        ],
        "High-value controlled drug dispense may require dual verification/approval.",
        [
            "POST /api/hms/pharmacy/orders/{id}/verify",
            "POST /api/hms/pharmacy/dispense",
            "POST /api/hms/pharmacy/returns",
        ],
        ["MedicationDispensed", "MedicationReturned", "BillableEventCreated"],
        ["ClinicalOrderPlaced", "StockAvailabilityChanged", "ItemChanged"],
        ["Out-of-stock to clinician", "Controlled drug dual-verify prompts"],
        ["Dispense volume", "Substitution log", "Controlled drug register"],
        "Dispense records immutable and highly regulated; retention extended for controlled substances as configured.",
        [
            "Dispense posting uses idempotency key and stock reservation to avoid oversell.",
            "Concurrent dispenses serialize per batch.",
        ],
        ["Dispense confirm P95 < 500ms excluding printer"],
        ["INV stock/batches", "HMS Billing/EMR/MAR", "FIN revenue posting", "HRIS credentials"],
        [
            "Successful dispense reduces stock and adds charge.",
            "Expired batch rejected at allocation.",
            "Reorder breach after dispense creates purchase requisition (via INV).",
        ],
        ["Drug-drug interaction engine can be rules-lite initially."],
    ),
    (
        "09-emr-ehr.md",
        "Medical Records (EMR/EHR)",
        "EMR",
        "§3.1 Medical Records; §3.2 clinical orders hub",
        "Longitudinal patient chart, clinical documentation, order entry, results inbox, and care timeline.",
        "Population health research warehouse; full FHIR external ecosystem in later phases.",
        ["Clinicians", "Clinical Coders", "Medical Records Officer", "Nurses"],
        [
            "Maintain longitudinal chart across OPD/IPD/ER/OT encounters.",
            "Support structured and narrative clinical notes with sign/amend.",
            "Provide CPOE for labs, radiology, medications, procedures.",
            "Display results/reports posted from LIS/RIS and dispense summaries.",
            "Enforce credential gates on order sign and note sign.",
            "Support problem list, allergies, and diagnosis coding entries.",
        ],
        """Note: `Draft -> Signed -> Amended`.
Order: `Draft -> Signed -> InFulfillment -> Completed | Cancelled`.""",
        ["`ClinicalNote`", "`ClinicalOrder`", "`Allergy`", "`Problem`", "`EncounterChart` projection"],
        [
            "Signed notes are immutable; corrections via amendment.",
            "Allergy hard-stop/warn on medication order per severity policy.",
            "Orders require patient encounter context.",
        ],
        "Break-glass chart access uses FND IAM policy.",
        [
            "POST /api/hms/emr/notes",
            "POST /api/hms/emr/notes/{id}/sign",
            "POST /api/hms/emr/orders",
            "GET /api/hms/emr/chart/{patientId}",
        ],
        ["ClinicalNoteSigned", "ClinicalOrderPlaced", "ClinicalOrderCancelled"],
        ["LabResultPosted", "RadiologyReportPosted", "MedicationDispensed", "EmployeeCredentialStatusChanged"],
        ["Critical results", "Unsigned draft aging for clinicians"],
        ["Chart access log", "Order volume by type"],
        "EMR is primary clinical system of record; strict PHI controls; amendment history preserved.",
        ["Note sign concurrency safe", "Order sign idempotent"],
        ["Chart summary load P95 < 1s for recent encounters"],
        ["All HMS clinical sub-modules", "HRIS credentials", "FND docs for attachments"],
        [
            "Signed lab order appears in LIS worklist.",
            "Lapsed clinician credential blocks new order sign.",
        ],
        ["FHIR export optional later; internal API first."],
    ),
    (
        "10-billing-claims.md",
        "Billing & Claims / Insurance",
        "BIL",
        "§3.1 Billing & claims; §3.2 steps 7–9; §3.3 billable events -> Financials",
        "Real-time charge accumulation, patient billing, insurance claim package assembly, and handoff to Financials AR.",
        "Insurer portal replacement; complex national DRG grouper beyond configurable packages initially.",
        ["Billing Officer", "Cashier", "Insurance/TPA Desk", "Finance AR (consumer)"],
        [
            "Accumulate charges from consultation, diagnostics, pharmacy, bed, OT, nursing, and other services in real time.",
            "Generate invoices split between self-pay and insurance/TPA portions.",
            "Assemble claim packages for TPA/insurer submission.",
            "Record payments/co-pay at cashier and emit AR events.",
            "Support discounts/waivers under approval policy.",
            "Track claim status updates toward settlement with Financials.",
        ],
        """Bill: `Open -> Interim -> Finalized -> PartiallyPaid -> Paid | WrittenOff`.
Claim: `Draft -> Submitted -> Accepted | PartiallyPaid | Denied -> Appealed -> Settled`.""",
        ["`Charge`", "`Invoice`", "`InvoiceLine`", "`Claim`", "`ClaimLine`", "`PaymentReceipt`"],
        [
            "Every charge references patient, encounter, charge code, amount, taxes, cost center.",
            "Finalization blocked if mandatory coding missing when policy requires.",
            "Billable events must be idempotent to prevent double charging.",
        ],
        "Discounts above threshold and write-offs require approval via FND engine.",
        [
            "POST /api/hms/billing/charges",
            "POST /api/hms/billing/invoices/{id}/finalize",
            "POST /api/hms/billing/claims",
            "POST /api/hms/billing/payments",
        ],
        ["BillableEventCreated", "InvoiceFinalized", "ClaimSubmitted", "PaymentReceived"],
        ["MedicationDispensed", "LabResultPosted", "OtImplantUsed", "PatientAdmitted", "OpdEncounterClosed"],
        ["Denial alerts", "High-balance alerts"],
        ["Daily collections", "Claim aging (ops)", "Charge mix"],
        "Financial artifacts retained per statutory policy; access restricted; payment voids audited.",
        [
            "Charge posting idempotent by sourceEventId.",
            "Payment allocation concurrency safe.",
        ],
        ["Charge post P95 < 300ms"],
        ["FIN AR/GL", "FND Approvals", "All HMS charge sources"],
        [
            "Pharmacy dispense creates charge without manual re-entry.",
            "Final invoice split self-pay vs insurance correctly.",
            "Payment posts receivable update in Financials.",
        ],
        ["Tax rules localized via FIN tax configuration."],
    ),
    (
        "11-discharge-follow-up.md",
        "Discharge & Follow-up",
        "DIS",
        "§3.1 Discharge; §3.2 steps 8–9",
        "Discharge reconciliation, discharge summary, follow-up appointment creation, prescription handoff, and post-discharge claim tracking handoff.",
        "Full remote patient monitoring.",
        ["Attending Physician", "Ward Nurse", "Billing Officer", "Medical Records"],
        [
            "Initiate discharge with clinical criteria checklist.",
            "Reconcile final bill before discharge completion (policy-configurable).",
            "Generate discharge summary and instructions.",
            "Create follow-up appointment and hand off outpatient prescription.",
            "Trigger insurance outstanding tracking in Financials.",
            "Release bed on discharge completion.",
        ],
        """Discharge: `Initiated -> ClinicalClearance -> BillingClearance -> Completed | Cancelled`.""",
        ["`DischargeProcess`", "`DischargeSummary`", "follow-up appointment link", "prescription handoff"],
        [
            "Cannot complete discharge with incomplete mandatory summary sections.",
            "Open critical results may warn/block per policy.",
            "Bed release only after completion.",
        ],
        "Discharge against unpaid self-pay balance may require waiver approval.",
        [
            "POST /api/hms/discharge",
            "POST /api/hms/discharge/{id}/summary",
            "POST /api/hms/discharge/{id}/complete",
        ],
        ["DischargeCompleted", "FollowUpScheduled", "ClaimSubmissionRequested"],
        ["InvoiceFinalized", "PaymentReceived"],
        ["Pending clearance alerts"],
        ["Discharge volume", "Discharge delay reasons"],
        "Discharge summaries are legal medical records; retention with clinical record policy.",
        ["Complete discharge saga compensates on failure (no silent bed leak)"],
        ["Discharge complete under 3s excluding user input"],
        ["HMS IPD/Billing/Pharmacy/EMR", "FIN AR claims"],
        [
            "Completed discharge frees bed and finalizes clinical summary.",
            "Follow-up appointment visible in front office schedule.",
            "Outstanding insurance portion tracked in AR.",
        ],
        ["Patient portal visibility Phase 4."],
    ),
]

for file, title, code, source, scope, exclusions, actors, functional, workflow, entities, rules, approvals, apis, eout, ein, notif, reports, audit, fails, nfr, deps, ac, assumptions in HMS_SUBS:
    write(
        f"01-hms/{file}",
        req_file(
            title, "HMS", code, source, scope, exclusions, actors, functional, workflow, entities, rules, approvals, apis, eout, ein, notif, reports, audit, fails, nfr, deps, ac, assumptions
        ),
    )

print("HMS written")

# Continue in part 2 - will be same file
print("Part1 done", ROOT)
