# Radiology / RIS / PACS Integration

| Field | Value |
|---|---|
| Module | HMS |
| Sub-module | RIS |
| Status | Draft — pending verification |
| Source | §3.1 Radiology/PACS; §3.2 imaging fulfillment |

## 1. Scope
Imaging order management, scheduling, report creation, and PACS study linkage with auto-post to EMR.

## 2. Exclusions
Replacing vendor PACS; advanced 3D workstation.

## 3. Actors and Permissions
- Radiographer
- Radiologist
- RIS Clerk
- Ordering Clinician

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| HMS-RIS-FR-001 | Accept radiology orders and schedule modalities. |
| HMS-RIS-FR-002 | Track study acquisition status and PACS accession/study UIDs. |
| HMS-RIS-FR-003 | Create/sign radiology reports. |
| HMS-RIS-FR-004 | Auto-post signed reports to EMR. |
| HMS-RIS-FR-005 | Post imaging charges per protocol. |

## 5. Workflow and State Transitions
Study: `Ordered -> Scheduled -> Acquired -> Reporting -> Reported | Cancelled`.

## 6. Data / Entities and Validation
- `RadiologyOrder`
- `ImagingStudy`
- `RadiologyReport`
- PACS identifiers

## 7. Business Rules
| ID | Rule |
|---|---|
| HMS-RIS-BR-001 | Only radiologist role can finalize diagnostic report. |
| HMS-RIS-BR-002 | Report amendments versioned. |
| HMS-RIS-BR-003 | PACS link optional for MVP with manual acquisition confirmation. |

## 8. Approvals
After-hours report privilege overrides audited.

## 9. APIs and Module Ownership
**Owner:** HMS

### APIs
- `POST /api/hms/ris/orders/accept`
- `POST /api/hms/ris/studies/{id}/acquire`
- `POST /api/hms/ris/reports`
- `POST /api/hms/ris/reports/{id}/sign`

### Events Published
- `RadiologyOrderAccepted`
- `RadiologyReportPosted`

### Events Consumed
- `ClinicalOrderPlaced`

## 10. Notifications
- STAT study alerts
- Unsigned report aging

## 11. Reports
- Modality utilization
- Report TAT

## 12. Audit, Retention, and Privacy
Imaging reports clinical PHI; PACS URLs access-controlled; audit downloads/views of reports.

## 13. Failure, Idempotency, and Concurrency
- Sign report idempotent
- Accession uniqueness

## 14. Non-Functional Requirements
- Report availability in EMR < 5s after sign

## 15. Dependencies
- HMS EMR/Billing
- External PACS optional

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| HMS-RIS-AC-001 | Signed report visible in EMR. |
| HMS-RIS-AC-002 | STAT order prioritized on worklist. |

## 17. Open Assumptions
- DICOM integration can be adapter-based in Phase 2+.

## 18. Source Traceability
Mapped from `§3.1 Radiology/PACS; §3.2 imaging fulfillment` in `Healthcare-ERP-Pathway-and-Workflow.md`.
