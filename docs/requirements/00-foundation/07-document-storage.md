# Document Storage

| Field | Value |
|---|---|
| Module | FND |
| Sub-module | DOC |
| Status | Draft — pending verification |
| Source | §4 HRIS documents/licenses; clinical attachments; vendor certificates |

## 1. Scope
Secure document vault for licenses, clinical attachments, vendor certificates, and financial artifacts with virus-scan hook and access control.

## 2. Exclusions
Full DAM/PACS image archive (RIS/PACS owns imaging binaries/integration).

## 3. Actors and Permissions
- All authorized users — upload/download per ACL
- Document Admin — retention classes and quotas

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| FND-DOC-FR-001 | Documents shall be stored encrypted at rest with module/entity linkage metadata. |
| FND-DOC-FR-002 | Access shall require permission on the owning business entity. |
| FND-DOC-FR-003 | Uploads shall enforce type/size limits and optional malware scan gate. |
| FND-DOC-FR-004 | Versioning shall be supported for replaceable documents (e.g., renewed license). |
| FND-DOC-FR-005 | Deletion shall be soft-delete/legal-hold aware. |

## 5. Workflow and State Transitions
`Uploading -> Quarantined -> Available -> Superseded -> Deleted(soft)`.
Legal hold blocks delete.

## 6. Data / Entities and Validation
- `DocumentObject`, `DocumentVersion`, `DocumentLink(entityType, entityId)`, `LegalHold`

## 7. Business Rules
| ID | Rule |
|---|---|
| FND-DOC-BR-001 | Download URLs are short-lived and scoped. |
| FND-DOC-BR-002 | Clinical documents inherit patient access rules from HMS. |

## 8. Approvals
Bulk purge requires Compliance approval.

## 9. APIs and Module Ownership
**Owner:** FND

### APIs
- `POST /api/fnd/documents (multipart or signed upload)`
- `GET /api/fnd/documents/{id}`
- `GET /api/fnd/documents/{id}/content`
- `POST /api/fnd/documents/{id}/versions`

### Events Published
- `DocumentAvailable`
- `DocumentSuperseded`

### Events Consumed
- None

## 10. Notifications
- Scan failure notice to uploader

## 11. Reports
- Storage usage by module
- Expiring linked credentials documents

## 12. Audit, Retention, and Privacy
Documents classified by sensitivity. Retention tied to entity class. Access audited.

## 13. Failure, Idempotency, and Concurrency
- Upload initiation idempotent by uploadSessionId.
- Concurrent version upload creates distinct versions with monotonic numbers.

## 14. Non-Functional Requirements
- Support files up to configurable max (default 25MB non-DICOM).
- Signed download URL TTL default 5 minutes.

## 15. Dependencies
- FND IAM
- FND Audit
- Object storage provider

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| FND-DOC-AC-001 | Uploading employee license makes document retrievable only to authorized HR/credential roles. |
| FND-DOC-AC-002 | Quarantined file is not downloadable by standard users. |

## 17. Open Assumptions
- Object storage is S3-compatible or local emulator for development.

## 18. Source Traceability
Mapped from `§4 HRIS documents/licenses; clinical attachments; vendor certificates` in `Healthcare-ERP-Pathway-and-Workflow.md`.
