# Human Resource Information System (HRIS) — Module Overview

| Field | Value |
|---|---|
| Module code | `HRIS` |
| Implementation phase | Phase 3 full; employee/credentials earlier as dependency for HMS gates |
| Source | Blueprint §4 |

## Purpose
Hire-to-retire workforce management including credentialing, 24×7 rostering, payroll inputs, and org hierarchy used by clinical scheduling and procurement approvals.

## Sub-modules
| Document | Summary |
|---|---|
| [Recruitment](01-recruitment.md) | Requisition to offer |
| [Onboarding & Employee Master](02-onboarding-employee-master.md) | Employee master creation |
| [Credentialing](03-credentialing.md) | Licenses, privileges, expiry |
| [Roster & Attendance](04-roster-attendance.md) | Shifts and attendance |
| [Leave Management](05-leave.md) | Leave requests and coverage |
| [Payroll & Compliance](06-payroll-compliance.md) | Payroll run and statutory |
| [Performance](07-performance.md) | Appraisals |
| [Training / CME](08-training-cme.md) | CME and renewals |
| [Employee Self-Service](09-self-service.md) | ESS portal |
| [Exit Management](10-exit.md) | Resignation/termination and FnF |

## Master Data Ownership
- Employee master
- Org hierarchy
- Credentials/privileges
- Roster/attendance/leave
- Payroll results

## Master Data Consumed
- FND approvals/IAM/docs
- FIN GL for payroll posting
- HMS scheduling consumers

## Integration Summary
This module publishes domain events through the Foundation integration hub and never writes directly into another module's tables. Cross-module workflows are specified under `06-cross-module-workflows/`.

## Verification Gate
Implementation of this module starts only after:
1. All sub-module requirement files are approved.
2. Foundation contracts used by this module are approved.
3. Acceptance criteria IDs are linked in the traceability register.
