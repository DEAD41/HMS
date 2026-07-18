# Data Governance, Privacy & Retention

| Field | Value |
|---|---|
| Module | FND |
| Sub-module | GOV |
| Status | Draft — pending verification |
| Source | §9 Regulatory & compliance |

## 1. Scope
Enterprise policies for privacy, consent, retention, legal hold, and data residency covering clinical, HR, financial, and vendor data.

## 2. Exclusions
External DLP product replacement; patient portal consent UX details belong partly to HMS portals.

## 3. Actors and Permissions
- Compliance Officer — policies
- Data Protection Officer — privacy requests
- Module owners — implement classification

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| FND-GOV-FR-001 | All personal data entities shall declare sensitivity classification. |
| FND-GOV-FR-002 | Retention schedules shall be configurable by data class and jurisdiction. |
| FND-GOV-FR-003 | Legal hold shall suspend purge. |
| FND-GOV-FR-004 | Subject access / export / rectification workflows shall be supported with module participation. |
| FND-GOV-FR-005 | Production data shall not be copied to non-prod without anonymization controls. |

## 5. Workflow and State Transitions
Policy: `Draft -> Active -> Retired`.
PrivacyRequest: `Received -> InProgress -> Completed | Rejected`.

## 6. Data / Entities and Validation
- `DataClass`, `RetentionPolicy`, `LegalHold`, `PrivacyRequest`

## 7. Business Rules
| ID | Rule |
|---|---|
| FND-GOV-BR-001 | Clinical data retention overrides generic defaults when stricter. |
| FND-GOV-BR-002 | Financial postings are never physically deleted within statutory period. |

## 8. Approvals
Activation of retention policy changes requires Compliance approval.

## 9. APIs and Module Ownership
**Owner:** FND

### APIs
- `GET/POST /api/fnd/governance/policies`
- `POST /api/fnd/governance/privacy-requests`
- `POST /api/fnd/governance/legal-holds`

### Events Published
- `PrivacyRequestCompleted`
- `LegalHoldApplied`

### Events Consumed
- None

## 10. Notifications
- DPO notified on new privacy request

## 11. Reports
- Retention upcoming purges
- Privacy request SLA

## 12. Audit, Retention, and Privacy
Governance configuration changes fully audited. Privacy request handling audited end-to-end.

## 13. Failure, Idempotency, and Concurrency
- Purge jobs are dry-run capable and idempotent.
- Holds always win over purge.

## 14. Non-Functional Requirements
- Policy evaluation available synchronously for delete operations.

## 15. Dependencies
- FND Audit
- All modules

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| FND-GOV-AC-001 | Record under legal hold cannot be purged. |
| FND-GOV-AC-002 | Privacy export includes data from participating modules for a subject. |

## 17. Open Assumptions
- Jurisdiction pack (e.g., PK/US/EU) selected at deployment.

## 18. Source Traceability
Mapped from `§9 Regulatory & compliance` in `Healthcare-ERP-Pathway-and-Workflow.md`.
