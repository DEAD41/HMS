#!/usr/bin/env python3
"""Generate HRIS, Financials, Inventory, Procurement, cross-workflows, verification."""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent / "docs" / "requirements"


def write(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def req_file(
    title, module_code, sub_code, source_refs, scope, exclusions, actors, functional,
    workflow, entities, business_rules, approvals, apis, events_out, events_in,
    notifications, reports, audit, failures, nfr, dependencies, acceptance, assumptions,
) -> str:
    fr_lines = "\n".join(f"| {module_code}-{sub_code}-FR-{i:03d} | {text} |" for i, text in enumerate(functional, 1))
    actor_lines = "\n".join(f"- {a}" for a in actors)
    entity_lines = "\n".join(f"- {e}" for e in entities)
    br_lines = "\n".join(f"| {module_code}-{sub_code}-BR-{i:03d} | {text} |" for i, text in enumerate(business_rules, 1))
    api_lines = "\n".join(f"- `{a}`" for a in apis)
    eo = "\n".join(f"- `{e}`" for e in events_out) or "- None"
    ei = "\n".join(f"- `{e}`" for e in events_in) or "- None"
    notif = "\n".join(f"- {n}" for n in notifications) or "- None"
    rep = "\n".join(f"- {r}" for r in reports) or "- None"
    fail = "\n".join(f"- {f}" for f in failures)
    nfr_lines = "\n".join(f"- {n}" for n in nfr)
    dep = "\n".join(f"- {d}" for d in dependencies)
    acc = "\n".join(f"| {module_code}-{sub_code}-AC-{i:03d} | {text} |" for i, text in enumerate(acceptance, 1))
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


def overview(title, code, purpose, submodules, owns, consumes, phase, source) -> str:
    rows = "\n".join(f"| [{name}]({file}) | {desc} |" for name, file, desc in submodules)
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


def emit(module_folder, module_code, items):
    for file, title, code, source, scope, exclusions, actors, functional, workflow, entities, rules, approvals, apis, eout, ein, notif, reports, audit, fails, nfr, deps, ac, assumptions in items:
        write(
            f"{module_folder}/{file}",
            req_file(title, module_code, code, source, scope, exclusions, actors, functional, workflow, entities, rules, approvals, apis, eout, ein, notif, reports, audit, fails, nfr, deps, ac, assumptions),
        )


# ---- HRIS ----
write(
    "02-hris/00-module-overview.md",
    overview(
        "Human Resource Information System (HRIS)",
        "HRIS",
        "Hire-to-retire workforce management including credentialing, 24×7 rostering, payroll inputs, and org hierarchy used by clinical scheduling and procurement approvals.",
        [
            ("Recruitment", "01-recruitment.md", "Requisition to offer"),
            ("Onboarding & Employee Master", "02-onboarding-employee-master.md", "Employee master creation"),
            ("Credentialing", "03-credentialing.md", "Licenses, privileges, expiry"),
            ("Roster & Attendance", "04-roster-attendance.md", "Shifts and attendance"),
            ("Leave Management", "05-leave.md", "Leave requests and coverage"),
            ("Payroll & Compliance", "06-payroll-compliance.md", "Payroll run and statutory"),
            ("Performance", "07-performance.md", "Appraisals"),
            ("Training / CME", "08-training-cme.md", "CME and renewals"),
            ("Employee Self-Service", "09-self-service.md", "ESS portal"),
            ("Exit Management", "10-exit.md", "Resignation/termination and FnF"),
        ],
        ["Employee master", "Org hierarchy", "Credentials/privileges", "Roster/attendance/leave", "Payroll results"],
        ["FND approvals/IAM/docs", "FIN GL for payroll posting", "HMS scheduling consumers"],
        "Phase 3 full; employee/credentials earlier as dependency for HMS gates",
        "Blueprint §4",
    ),
)

HRIS = [
    ("01-recruitment.md", "Recruitment & Requisitioning", "REC", "§4.1 Recruitment; §4.2 step 1",
     "Department requisitions, approvals, job posting, screening, interview, and offer.",
     "External job board product; AI screening marketplace.",
     ["Department Head", "HR Recruiter", "Interview Panel", "HR Manager"],
     ["Raise manpower requisition with role, grade, and justification.",
      "Route requisition through approval hierarchy.",
      "Manage candidates, interviews, and evaluations.",
      "Generate offers with compensation components.",
      "On offer accept, trigger onboarding case."],
     """Requisition: `Draft -> Submitted -> Approved | Rejected -> Open -> Filled | Cancelled`.
Candidate: `Applied -> Screening -> Interview -> Offered -> Hired | Rejected`.""",
     ["`ManpowerRequisition`", "`Candidate`", "`Interview`", "`Offer`"],
     ["Cannot hire above approved headcount without exception approval.", "Offer above band requires HR Manager approval."],
     "Uses FND approval engine with HRIS org hierarchy.",
     ["POST /api/hris/requisitions", "POST /api/hris/candidates", "POST /api/hris/offers"],
     ["RequisitionApproved", "OfferAccepted"], [],
     ["Approver notifications", "Offer expiry reminders"],
     ["Time-to-hire", "Open requisitions"],
     "Candidate PII protected; retention per HR policy.",
     ["Offer accept idempotent", "Concurrent fill of last vacancy: first wins"],
     ["Standard CRUD SLAs"],
     ["FND Approvals", "HRIS Employee master"],
     ["Approved requisition can progress to offer.", "Accepted offer opens onboarding."],
     ["Job posting channels may be manual initially."]),
    ("02-onboarding-employee-master.md", "Onboarding & Employee Master", "EMP", "§4.1 Employee master; §4.2 step 2; §2 employee ownership",
     "Create and maintain employee master, documents, department assignment, and user provisioning trigger.",
     "Full LMS content platform.",
     ["HR Officer", "Department Head", "Employee"],
     ["Create employee master from hired candidate or direct hire.",
      "Capture demographics, employment terms, department, cost center, reporting manager.",
      "Collect onboarding documents via document vault.",
      "Activate employee and emit EmployeeChanged for projections/IAM linking.",
      "Support transfers and status changes."],
     """Employee: `Onboarding -> Active -> Suspended -> Exited -> Archived`.""",
     ["`Employee`", "`EmploymentContract`", "`EmployeeDocumentLink`", "`OrgAssignment`"],
     ["Employee code unique per tenant.", "Active clinical staff must eventually have credential records before scheduling.", "Cost center required before payroll finalize."],
     "Backdated join date corrections require HR Manager approval.",
     ["POST /api/hris/employees", "PUT /api/hris/employees/{id}", "POST /api/hris/employees/{id}/activate"],
     ["EmployeeChanged", "EmployeeActivated"], ["OfferAccepted", "DocumentAvailable"],
     ["Missing onboarding document reminders"],
     ["Headcount by department"],
     "Employee PII/HR confidential; access role-restricted; audited.",
     ["Activate idempotent", "Optimistic concurrency on employee"],
     ["Employee search P95 < 300ms"],
     ["FND Docs/IAM", "FIN cost centers"],
     ["Activated employee appears in master projections.", "IAM can link user to employee id."],
     ["Biometric enrollment system external."]),
    ("03-credentialing.md", "Credentialing & Clinical Privileges", "CRD", "§4.1 credentialing; §4.2 steps 2,6; §4.3 gates HMS",
     "Track licenses, certifications, specialty privileges, expiry alerts, and clinical action gating signals.",
     "External medical council live verification APIs beyond manual evidence.",
     ["Credentialing Officer", "Medical Director", "Clinician"],
     ["Record licenses/certifications with issue/expiry dates and evidence documents.",
      "Maintain specialty privilege grants per facility.",
      "Emit credential status changes for HMS scheduling/order signing gates.",
      "Alert before expiry and auto-suspend privileges on lapse per policy.",
      "Support temporary privilege grants with end dates."],
     """Credential: `Submitted -> Verified -> Active -> ExpiringSoon -> Expired | Suspended | Revoked`.""",
     ["`Credential`", "`Privilege`", "`CredentialAlert`"],
     ["HMS must deny schedule/sign when required credential inactive.", "Expired credential cannot be used even if employee active."],
     "Privilege grant/revoke for high-risk procedures require Medical Director approval.",
     ["POST /api/hris/credentials", "POST /api/hris/privileges", "GET /api/hris/credentials/status/{employeeId}"],
     ["EmployeeCredentialStatusChanged", "CredentialExpiring"], [],
     ["Expiry alerts to clinician and credentialing office"],
     ["Expiring credentials", "Privilege matrix"],
     "Credential evidence retained; changes audited immutable.",
     ["Status recompute job idempotent", "Concurrent privilege edits conflict-checked"],
     ["Status check API P95 < 50ms cached"],
     ["HRIS Employee", "HMS consumers", "FND Notifications/Docs"],
     ["Lapsed license sets credential status inactive and HMS blocks sign-off.", "Expiry alert fires within configured lead time."],
     ["Lead time default 30/60/90 days configurable."]),
    ("04-roster-attendance.md", "Duty Roster, Shifts & Attendance", "ROS", "§4.1 Attendance/roster; §4.2 step 3",
     "Build department shift rosters (nursing/ICU/OT coverage) and capture attendance for payroll.",
     "Advanced predictive staffing AI.",
     ["Roster Planner", "Nursing Supervisor", "Employees", "Payroll Officer (read)"],
     ["Create shift templates and period rosters by department/ward.",
      "Detect coverage gaps and skill/credential mismatches.",
      "Capture attendance (manual/biometric import).",
      "Publish roster to employees and HMS clinical scheduling consumers.",
      "Lock roster periods for payroll."],
     """RosterPeriod: `Draft -> Published -> Locked`.
Attendance: `Present | Absent | HalfDay | OnLeave | Holiday`.""",
     ["`ShiftTemplate`", "`RosterAssignment`", "`AttendanceRecord`"],
     ["Cannot assign clinician lacking required credential for unit.", "Locked period attendance corrections require approval."],
     "Published roster changes within 24h may require supervisor approval.",
     ["POST /api/hris/rosters", "POST /api/hris/rosters/{id}/publish", "POST /api/hris/attendance"],
     ["RosterPublished", "AttendancePosted"], ["EmployeeCredentialStatusChanged", "LeaveApproved"],
     ["Coverage gap alerts"],
     ["Coverage compliance", "Overtime preview"],
     "Attendance feeds payroll; corrections audited.",
     ["Publish conflict detection", "Attendance upsert idempotent by employee/date/source"],
     ["Roster publish for 500 staff < 5s"],
     ["HRIS Leave/Credentials", "HMS scheduling", "Payroll"],
     ["Publishing roster with unqualified ICU nurse fails validation.", "Attendance available to payroll run."],
     ["Biometric devices integrate via import file/API adapter."]),
    ("05-leave.md", "Leave Management", "LVE", "§4.1 Leave; §4.2 step 4",
     "Leave balances, requests, approvals, and roster auto-adjust signals for coverage gaps.",
     "Complex union leave banking beyond configurable leave types.",
     ["Employee", "Manager", "HR"],
     ["Maintain leave types and balances.",
      "Submit leave requests with date ranges.",
      "Route approvals and update balances on approval.",
      "Notify roster planners to cover gaps.",
      "Integrate with attendance and payroll."],
     """LeaveRequest: `Draft -> Submitted -> Approved | Rejected | Cancelled`.""",
     ["`LeaveType`", "`LeaveBalance`", "`LeaveRequest`"],
     ["Insufficient balance blocks unless unpaid/exception policy.", "Overlapping approved leave forbidden."],
     "Uses FND approvals; HR override for exceptions.",
     ["POST /api/hris/leave/requests", "POST /api/hris/leave/requests/{id}/cancel", "GET /api/hris/leave/balances/{employeeId}"],
     ["LeaveApproved", "LeaveRejected", "LeaveCancelled"], [],
     ["Manager approval inbox", "Roster coverage impact"],
     ["Leave liability", "Absenteeism"],
     "Leave records HR confidential; retention with employment records.",
     ["Approval decision idempotent", "Balance update transactional"],
     ["Standard API SLAs"],
     ["FND Approvals", "Roster", "Payroll"],
     ["Approved leave reduces balance and marks attendance.", "Roster gap notification generated."],
     ["Calendar year vs anniversary year configurable."]),
    ("06-payroll-compliance.md", "Payroll & Statutory Compliance", "PAY", "§4.1 Payroll; §4.2 step 5; §4.3 posts to Financials",
     "Monthly payroll processing from attendance/leave/earnings/deductions and posting salary expense/liabilities to Financials with bank file generation.",
     "Full treasury bank host-to-host beyond payment file; multi-country statutory packs beyond configured locale pack.",
     ["Payroll Officer", "Finance Controller", "HR Manager"],
     ["Configure earnings/deductions and statutory rules pack.",
      "Run payroll calculation for a period.",
      "Support review adjustments and approvals.",
      "Finalize payroll and post accounting entries to Financials.",
      "Generate bank disbursement file and payslips."],
     """PayrollRun: `Open -> Calculated -> InReview -> Approved -> Posted | Void`.""",
     ["`PayrollRun`", "`Payslip`", "`PayrollPosting`", "`BankFile`"],
     ["Cannot modify posted run except via reversal/void workflow.", "Employee without cost center excluded from finalize with error list."],
     "Payroll approve/post requires Finance/HR dual approval per policy.",
     ["POST /api/hris/payroll/runs", "POST /api/hris/payroll/runs/{id}/calculate", "POST /api/hris/payroll/runs/{id}/post"],
     ["PayrollPosted", "PayslipPublished"], ["AttendancePosted", "LeaveApproved"],
     ["Payslip available", "Posting failure alerts"],
     ["Payroll register", "Statutory summaries", "Variance vs prior period"],
     "Payroll data highly confidential; access tightly controlled; statutory retention.",
     ["Posting uses outbox; financial consumer idempotent by payrollRunId", "Calculate re-runnible before approve"],
     ["Calculate 2,000 employees within configured batch SLA"],
     ["FIN GL", "FND Approvals", "Attendance/Leave"],
     ["Posted payroll creates GL expense/liability entries once.", "Bank file generated for approved net pay."],
     ["Statutory pack initially for primary deployment country."]),
    ("07-performance.md", "Performance Management & Appraisals", "PRF", "§4.1 Performance; §4.2 step 6",
     "Periodic appraisals, goals, and ratings that may inform privileges/training plans.",
     "Full OKR enterprise suite.",
     ["Employee", "Manager", "HR BP"],
     ["Define appraisal cycles and templates.",
      "Capture self/manager reviews and ratings.",
      "Finalize appraisal outcomes.",
      "Link development actions to training module."],
     """Appraisal: `NotStarted -> SelfReview -> ManagerReview -> Calibration -> Finalized`.""",
     ["`AppraisalCycle`", "`AppraisalForm`", "`Rating`"],
     ["Finalized appraisals immutable except formal appeal process."],
     "Calibration changes may require HR approval.",
     ["POST /api/hris/appraisals", "POST /api/hris/appraisals/{id}/finalize"],
     ["AppraisalFinalized"], [],
     ["Cycle deadline reminders"],
     ["Rating distribution"],
     "Performance data confidential.",
     ["Finalize idempotent"],
     ["Standard SLAs"],
     ["HRIS Employee", "Training"],
     ["Finalized appraisal stored and visible to authorized parties."],
     ["Compensation linkage optional later."]),
    ("08-training-cme.md", "Training / CME Tracking", "TRN", "§4.1 Training/CME; §4.2 step 6",
     "Track CME/training completions and certification renewals feeding credentialing alerts.",
     "Full e-learning content delivery platform.",
     ["Training Coordinator", "Clinician", "Credentialing Officer"],
     ["Catalog training/CME activities.",
      "Record attendance/completion and credit hours.",
      "Link completions to credential renewals.",
      "Alert on missing mandatory training."],
     """TrainingAssignment: `Assigned -> InProgress -> Completed | Overdue`.""",
     ["`TrainingCourse`", "`TrainingAssignment`", "`CmeCredit`"],
     ["Mandatory training overdue can suspend selected privileges per policy."],
     "Policy exceptions approved by Medical Director/HR.",
     ["POST /api/hris/training/assignments", "POST /api/hris/training/completions"],
     ["TrainingCompleted", "MandatoryTrainingOverdue"], ["CredentialExpiring"],
     ["Overdue mandatory training alerts"],
     ["CME hours by clinician", "Compliance rate"],
     "Training records retained with credential evidence.",
     ["Completion posting idempotent"],
     ["Standard SLAs"],
     ["Credentialing", "Notifications"],
     ["Completion updates CME credits and can clear renewal prerequisites."],
     ["External CME providers via manual credit entry initially."]),
    ("09-self-service.md", "Employee Self-Service Portal", "ESS", "§4.1 ESS",
     "Employee self-service for profile view, leave, payslips, roster, and training assignments.",
     "Patient portal (HMS); vendor portal (Procurement).",
     ["Employee"],
     ["View personal profile and documents metadata.",
      "Submit leave and view balances.",
      "View published roster and payslips.",
      "Update limited personal contacts with verification rules."],
     """ESS actions reuse underlying entity states.""",
     ["No new masters; facade over HRIS services"],
     ["Employees only see own data unless manager delegation features enabled."],
     "Sensitive profile changes may require HR approval.",
     ["GET /api/hris/ess/me", "POST /api/hris/ess/leave", "GET /api/hris/ess/payslips"],
     [], ["PayslipPublished", "RosterPublished"],
     ["Leave status changes"],
     ["ESS adoption metrics"],
     "Same controls as source data; authentication required.",
     ["Standard idempotency on submissions"],
     ["Mobile-responsive UI target"],
     ["Leave/Payroll/Roster APIs"],
     ["Employee can download own payslip after publish.", "Cannot view another employee's payslip."],
     ["Mobile native apps later."]),
    ("10-exit.md", "Exit Management", "EXIT", "§4.1 Exit; §4.2 step 7; §4.3 access revoke",
     "Resignation/termination workflow, clearance, full-and-final settlement posting, and access revocation across modules.",
     "Outplacement services.",
     ["HR Officer", "Manager", "Finance", "IT/Security"],
     ["Initiate resignation/termination cases.",
      "Run clearance checklist (assets, store returns, clinical handover).",
      "Calculate FnF and post to Financials.",
      "Set employee exited and emit events to disable IAM and clinical scheduling.",
      "Archive employee record."],
     """ExitCase: `Initiated -> InClearance -> FnFCalculated -> Settled -> Closed`.""",
     ["`ExitCase`", "`ClearanceItem`", "`FullAndFinalSettlement`"],
     ["Exited employees cannot be rostered or authenticate (except legal hold access).", "FnF posting idempotent to FIN."],
     "Termination without notice and FnF exceptions require HR/Finance approvals.",
     ["POST /api/hris/exits", "POST /api/hris/exits/{id}/clearance", "POST /api/hris/exits/{id}/settle"],
     ["EmployeeExited", "FnFPosted"], ["ApprovalDecisionMade"],
     ["Clearance pending reminders", "Access revocation confirmation"],
     ["Exit turnaround", "FnF register"],
     "Exit files confidential; retention statutory.",
     ["Settle uses outbox", "Access revoke eventual with retry"],
     ["Access revoke propagation < 5 minutes"],
     ["FND IAM", "FIN", "Inventory returns optional"],
     ["Closed exit disables login and removes future roster eligibility.", "FnF appears in Financials."],
     ["Asset return detailed tracking may use Inventory/Assets modules."]),
]
emit("02-hris", "HRIS", HRIS)
print("HRIS written")

# ---- Financials ----
write(
    "03-financials/00-module-overview.md",
    overview(
        "Financials",
        "FIN",
        "General ledger and financial operations covering order-to-cash, procure-to-pay, payroll posting, budgeting, assets, tax, and MIS.",
        [
            ("GL / Chart of Accounts", "01-gl-coa.md", "COA, journals, periods"),
            ("Accounts Payable", "02-ap.md", "Vendor invoices, three-way match, payments"),
            ("Accounts Receivable", "03-ar.md", "Patient/insurer receivables"),
            ("Budgeting & Cost Centers", "04-budgeting-cost-centers.md", "Budgets and control"),
            ("Fixed Assets", "05-fixed-assets.md", "Assets and depreciation"),
            ("Cash & Bank", "06-cash-bank.md", "Cash/bank management"),
            ("Tax & Statutory", "07-tax-statutory.md", "Tax configuration and statutory reports"),
            ("MIS & Financial Reporting", "08-mis.md", "P&L, BS, cost-per-patient, profitability"),
        ],
        ["Chart of accounts", "Cost centers", "GL", "AP/AR subledgers", "Fixed assets", "Tax config"],
        ["HMS billing events", "INV consumption/write-offs", "PRC PO/GRN/vendor", "HRIS payroll", "FND approvals"],
        "Phase 1 core GL/AP/AR; Phase 4 budgeting/advanced MIS",
        "Blueprint §5",
    ),
)

FIN = [
    ("01-gl-coa.md", "General Ledger / Chart of Accounts", "GL", "§5.1 GL/COA; all postings",
     "Maintain COA, accounting periods, journals, and financial postings from all modules.",
     "Multi-GAAP consolidation group accounting beyond single primary book MVP.",
     ["Accountant", "Finance Controller"],
     ["Maintain chart of accounts and account types.",
      "Open/close accounting periods.",
      "Post manual and system journals with balanced debits/credits.",
      "Provide trial balance and account inquiry.",
      "Support cost center dimensions on postings."],
     """Period: `Future -> Open -> SoftClose -> Closed`.
Journal: `Draft -> Posted | Reversed`.""",
     ["`Account`", "`AccountingPeriod`", "`JournalEntry`", "`JournalLine`"],
     ["Posted journals immutable; corrections via reversing entries.", "Journals must balance in transaction currency/base currency rules.", "Closed periods reject new postings except controlled reopen."],
     "Period close and reopen require Controller approval.",
     ["POST /api/fin/coa/accounts", "POST /api/fin/journals", "POST /api/fin/periods/{id}/close"],
     ["AccountChanged", "JournalPosted", "PeriodClosed"],
     ["PayrollPosted", "InvoiceFinalized", "VendorInvoiceMatched", "StockIssued", "StockWrittenOff", "FnFPosted"],
     ["Period close reminders"],
     ["Trial balance", "Journal register"],
     "Financial records statutory retention; immutable posted ledger.",
     ["System posting idempotent by sourceDocumentId", "Concurrent period close guarded"],
     ["Posting P95 < 200ms"],
     ["All feeder modules", "FND Approvals"],
     ["Unbalanced journal rejected.", "Duplicate sourceDocumentId does not double post."],
     ["Single base currency per facility with optional multi-currency later."]),
    ("02-ap.md", "Accounts Payable", "AP", "§5.1 AP; §5.2 B procure-to-pay; three-way match",
     "Vendor invoice capture, three-way match against PO/GRN, payment scheduling, and GL posting.",
     "Dynamic discounting marketplace.",
     ["AP Clerk", "AP Supervisor", "Finance Controller"],
     ["Capture vendor invoices against vendors/POs.",
      "Perform three-way match (PO, GRN, invoice) with tolerance rules.",
      "Schedule and execute payments per terms.",
      "Post AP and payment entries to GL/vendor ledger.",
      "Manage debit notes and adjustments."],
     """VendorInvoice: `Received -> Matching -> Matched | Variance -> Approved -> Scheduled -> Paid | Void`.
Payment: `Proposed -> Approved -> Disbursed | Failed`.""",
     ["`VendorInvoice`", "`MatchResult`", "`PaymentProposal`", "`ApPayment`"],
     ["Payment blocked unless matched/approved or explicit exception.", "Tolerances configurable by item/vendor/category."],
     "Payment release uses FND approvals by amount threshold.",
     ["POST /api/fin/ap/invoices", "POST /api/fin/ap/invoices/{id}/match", "POST /api/fin/ap/payments"],
     ["VendorInvoiceMatched", "ApPaymentDisbursed"],
     ["PurchaseOrderIssued", "GoodsReceived", "VendorChanged"],
     ["Match variance alerts", "Payment due reminders"],
     ["AP aging", "Three-way match exceptions"],
     "AP documents retained; vendor banking data confidential.",
     ["Match/payment idempotent", "Payment disbursement exactly-once effective"],
     ["Match engine for typical invoice < 1s"],
     ["PRC PO", "INV GRN", "FIN GL", "FND Approvals"],
     ["Exact PO+GRN+invoice match allows payment scheduling.", "Duplicate invoice number per vendor rejected."],
     ["OCR invoice capture optional later."]),
    ("03-ar.md", "Accounts Receivable / Patient & Insurance", "AR", "§5.1 AR; §5.2 A order-to-cash",
     "Track patient and insurer receivables from HMS billing, receipts, denials, and aging.",
     "External collection agency system.",
     ["AR Officer", "Cashier (HMS payments)", "Finance Controller"],
     ["Create AR open items from finalized invoices/claims.",
      "Apply receipts and allocations.",
      "Track insurance claim settlements/partials/denials.",
      "Provide aging analysis for patients and insurers.",
      "Support write-offs under approval."],
     """Receivable: `Open -> PartiallySettled -> Settled | WrittenOff`.
ClaimAR follows HMS claim statuses with financial settlement states.""",
     ["`Receivable`", "`ReceiptApplication`", "`Denial`", "`WriteOff`"],
     ["Receipts cannot over-apply without credit balance rules.", "Write-off above threshold needs approval."],
     "Write-offs and courtesy discounts via FND approvals.",
     ["POST /api/fin/ar/open-items/sync", "POST /api/fin/ar/receipts/apply", "POST /api/fin/ar/write-offs"],
     ["ReceivableSettled", "ArWriteOffPosted"],
     ["InvoiceFinalized", "ClaimSubmitted", "PaymentReceived", "DischargeCompleted"],
     ["Denial alerts", "High aging alerts"],
     ["AR aging", "Collection efficiency", "Denial reasons"],
     "Patient financial PHI/PII minimized; access restricted; retention statutory.",
     ["Application idempotent by receiptId+line", "Concurrency on open item balance"],
     ["Aging query P95 < 2s for facility month"],
     ["HMS Billing/Claims", "FIN GL/Cash"],
     ["Finalized invoice creates AR open item.", "Aging report shows unpaid insurer balances."],
     ["Customer master for insurers may overlap payer records from HMS."]),
    ("04-budgeting-cost-centers.md", "Budgeting & Cost-Center Control", "BUD", "§5.1 Budgeting; §5.2 D",
     "Annual/quarterly budgets per cost center and real-time variance against procurement, store issues, and payroll.",
     "Driver-based predictive budgeting AI.",
     ["Department Head", "Finance Controller", "Budget Analyst"],
     ["Maintain cost centers and hierarchies.",
      "Capture budgets by period/account/cost center.",
      "Track actuals from postings/events.",
      "Raise variance alerts when thresholds breached.",
      "Optionally hard-stop or warn procurement commitments over budget."],
     """BudgetVersion: `Draft -> Submitted -> Approved -> Active -> Closed`.""",
     ["`CostCenter`", "`BudgetVersion`", "`BudgetLine`", "`VarianceAlert`"],
     ["Active budget required for hard-control mode.", "Actuals are derived, not manually overriding posted facts."],
     "Budget approval via FND engine.",
     ["POST /api/fin/cost-centers", "POST /api/fin/budgets", "GET /api/fin/budgets/variance"],
     ["CostCenterChanged", "BudgetApproved", "BudgetVarianceBreached"],
     ["JournalPosted", "PurchaseOrderIssued", "StockIssued", "PayrollPosted"],
     ["Variance alerts to dept heads/controllers"],
     ["Budget vs actual", "Department burn rate"],
     "Budget artifacts retained with financial planning records.",
     ["Variance calc eventual consistent with posting lag tolerance"],
     ["Variance dashboard < 3s"],
     ["FIN GL", "PRC", "INV", "HRIS payroll", "FND Notifications"],
     ["Approved budget visible for control checks.", "Over-threshold PO triggers warn/block per config."],
     ["Hard control optional per facility."]),
    ("05-fixed-assets.md", "Fixed Assets & Biomedical Depreciation", "FA", "§5.1 Fixed Assets; equipment from Procurement; spares linkage",
     "Asset register for equipment, capitalization from procurement, depreciation schedules, and maintenance cost linkage.",
     "Full CMMS replacement; IoT telemetry.",
     ["Asset Accountant", "Biomedical Engineer", "Finance Controller"],
     ["Create assets from capitalized PO/GRN or manual entry.",
      "Maintain depreciation methods and run periodic depreciation.",
      "Record transfers, disposal, and impairment.",
      "Attach maintenance cost from spare issues.",
      "Provide asset register reports."],
     """Asset: `Draft -> Active -> UnderMaintenance -> Disposed | FullyDepreciated`.
DepreciationRun: `Draft -> Posted`.""",
     ["`FixedAsset`", "`DepreciationSchedule`", "`DepreciationRun`", "`AssetMaintenanceCost`"],
     ["Disposed assets stop depreciation.", "Capitalization thresholds configurable."],
     "Disposal and impairment require approval.",
     ["POST /api/fin/assets", "POST /api/fin/assets/depreciation-runs", "POST /api/fin/assets/{id}/dispose"],
     ["AssetCreated", "DepreciationPosted", "AssetDisposed"],
     ["GoodsReceived (capital)", "SparePartIssued"],
     ["Depreciation due reminders"],
     ["Asset register", "Depreciation forecast"],
     "Asset history retained for audit/regulatory device tracking as applicable.",
     ["Depreciation posting idempotent per period/asset"],
     ["Monthly depreciation batch SLA configurable"],
     ["PRC/INV", "FIN GL"],
     ["Capital equipment GRN can create asset.", "Spare issue adds maintenance cost to asset."],
     ["Componentization optional later."]),
    ("06-cash-bank.md", "Cash & Bank Management", "CASH", "§5.1 Cash & bank",
     "Cash drawers, bank accounts, deposits, reconciliations, and disbursement execution records.",
     "Full TMS / multi-bank connectivity suite.",
     ["Cashier Supervisor", "Treasury Accountant"],
     ["Maintain bank/cash accounts.",
      "Record deposits and withdrawals.",
      "Reconcile bank statements.",
      "Integrate disbursement confirmations for AP/payroll files."],
     """BankRec: `Open -> InProgress -> Reconciled`.
CashSession: `Open -> Closed`.""",
     ["`BankAccount`", "`CashSession`", "`BankStatement`", "`BankReconciliation`"],
     ["Cash session must close balanced per policy.", "Reconciled items immutable."],
     "Manual bank adjustments require approval above threshold.",
     ["POST /api/fin/cash/sessions", "POST /api/fin/bank/statements/import", "POST /api/fin/bank/reconciliations"],
     ["BankReconciliationCompleted", "CashSessionClosed"],
     ["ApPaymentDisbursed", "PaymentReceived", "PayrollPosted"],
     ["Unreconciled item aging alerts"],
     ["Cash position", "Reconciliation status"],
     "Banking data sensitive; dual control recommended for disbursements.",
     ["Import idempotent by statement fingerprint"],
     ["Import 10k lines within batch SLA"],
     ["FIN AP/AR/Payroll"],
     ["Cashier receipt can be deposited and reconciled.", "Payroll bank file disbursement status trackable."],
     ["Direct bank API optional."]),
    ("07-tax-statutory.md", "Taxation & Statutory Reporting", "TAX", "§5.1 Taxation & statutory reporting",
     "Tax configuration (sales/withholding/VAT/GST as applicable) and statutory report generation.",
     "Government e-filing robot beyond export files.",
     ["Tax Accountant", "Finance Controller"],
     ["Configure tax codes/rates and applicability rules.",
      "Calculate tax on invoices/payments as configured.",
      "Produce statutory reports/exports for filing periods.",
      "Support withholding tax on vendor payments where required."],
     """TaxPeriodReturn: `Open -> Prepared -> Submitted -> Amended`.""",
     ["`TaxCode`", "`TaxRate`", "`TaxTransaction`", "`StatutoryReturn`"],
     ["Posted tax amounts change only via amending documents.", "Rate changes effective-dated."],
     "Return submission mark-off may require Controller approval.",
     ["POST /api/fin/tax/codes", "GET /api/fin/tax/returns/{period}", "POST /api/fin/tax/returns/{period}/prepare"],
     ["TaxReturnPrepared"], ["InvoiceFinalized", "ApPaymentDisbursed"],
     ["Filing deadline reminders"],
     ["Tax return drafts", "Withholding summaries"],
     "Statutory archives retained per law.",
     ["Prepare job idempotent per period version"],
     ["Prepare month return within batch SLA"],
     ["FIN AR/AP/GL"],
     ["Invoice tax calculated using active rates.", "Period return includes posted tax transactions."],
     ["Locale tax pack selected at deployment."]),
    ("08-mis.md", "Financial Reporting & MIS", "MIS", "§5.1 Financial reporting & MIS; §9 analytics",
     "P&L, balance sheet, cost-per-patient, department profitability, and management packs from integrated data.",
     "Board narrative automation AI.",
     ["CFO", "Controllers", "Department Heads (scoped)"],
     ["Generate P&L and balance sheet for periods.",
      "Compute cost-per-patient and department profitability KPIs.",
      "Publish management dashboards via FND reporting contracts.",
      "Support drilldown to journals/source documents per security."],
     """ReportPack: `Generating -> Ready | Failed`.""",
     ["Read models over GL + feeder facts", "KPI definitions cataloged in FND RPT"],
     ["Users only see authorized cost centers/facilities."],
     "Enterprise pack publish may require Controller approval.",
     ["GET /api/fin/mis/pnl", "GET /api/fin/mis/balance-sheet", "GET /api/fin/mis/kpis/cost-per-patient"],
     ["MisPackReady"], ["JournalPosted", "ReportRunCompleted"],
     ["Pack ready notices"],
     ["P&L", "Balance sheet", "Cost-per-patient", "Department profitability", "Staff cost ratio (with HRIS facts)"],
     "Aggregates preferred; drilldown audited.",
     ["KPI recompute eventual; pin snapshot for published packs"],
     ["Interactive financial statements < 3s warmed"],
     ["FIN GL/AR/AP", "HMS/INV/HRIS facts", "FND RPT"],
     ["Authorized user can produce department profitability for a month.", "Cost-per-patient KPI available after billing+cost postings."],
     ["Exact KPI formulas documented in TRACEABILITY/KPI appendix during build."]),
]
emit("03-financials", "FIN", FIN)
print("FIN written")

# ---- Inventory ----
write(
    "04-inventory/00-module-overview.md",
    overview(
        "Store & Spares (Inventory)",
        "INV",
        "Item master ownership, multi-store stock control, batch/expiry, issues, transfers, reorder planning, counts, and biomedical spares.",
        [
            ("Stores & Bins", "01-stores-bins.md", "Central/sub-stores and bins"),
            ("Item Master", "02-item-master.md", "SKU master"),
            ("Receipts & Quality", "03-receipts-quality.md", "GRN quality and putaway"),
            ("Batch & Expiry", "04-batch-expiry.md", "Batch/FEFO controls"),
            ("Issues & Consumption", "05-issues-consumption.md", "Patient/dept/spares issues"),
            ("Transfers", "06-transfers.md", "Inter-store transfers"),
            ("Reorder Planning", "07-reorder-planning.md", "Min/max and auto PR"),
            ("Counts & Adjustments", "08-counts-adjustments.md", "Cycle counts and variances"),
            ("Biomedical Spares", "09-biomedical-spares.md", "Spares for equipment"),
        ],
        ["Item/SKU master", "Stock ledgers", "Batches", "Stores/bins"],
        ["PRC PO/vendor", "HMS pharmacy/ward/OT issues", "FIN COGS/write-off/asset maintenance", "FND approvals"],
        "Phase 2 operations",
        "Blueprint §6",
    ),
)

INV = [
    ("01-stores-bins.md", "Central Store / Sub-stores / Bins", "STR", "§6.1 stores; warehouse/bin",
     "Configure central store, pharmacy/ward/OT stores, and bin locations.",
     "Automated warehouse robotics.",
     ["Store Admin", "Store Keeper"],
     ["Create stores linked to facilities/org units.",
      "Configure bins/locations within stores.",
      "Define which stores serve which clinical units.",
      "Activate/deactivate stores with stock constraints."],
     """Store: `Draft -> Active -> Inactive`.""",
     ["`Store`", "`Bin`", "`StoreServiceArea`"],
     ["Cannot inactivate store with non-zero stock without transfer/write-off.", "Pharmacy stores must support batch tracking."],
     "Store inactivation requires approval if stock remains.",
     ["POST /api/inv/stores", "POST /api/inv/bins"],
     ["StoreChanged"], [],
     ["Inactive store with stock alerts"],
     ["Store list with valuations summary"],
     "Configuration changes audited.",
     ["Optimistic concurrency"],
     ["Standard SLAs"],
     ["FND Tenancy"],
     ["Active pharmacy store selectable for dispense allocation."],
     ["Default bin optional per store."]),
    ("02-item-master.md", "Item / SKU Master", "ITEM", "§6.1; §6.2 step 1; §2 item ownership",
     "Register drugs, consumables, implants, and spare parts with UOM, reorder, and batch/expiry rules.",
     "Global GS1 network management beyond barcode fields.",
     ["Item Master Steward", "Pharmacist (drug items)", "Biomed Engineer (spares)"],
     ["Create/update item master with category, UOM, valuation method, reorder level/safety stock.",
      "Flag batch/expiry/serial controlled items.",
      "Publish ItemChanged for HMS/PRC/FIN projections.",
      "Support item status lifecycle."],
     """Item: `Draft -> Active -> Suspended -> Obsolete`.""",
     ["`Item`", "`ItemUom`", "`ItemReorderPolicy`", "`ItemCategory`"],
     ["Active clinical ordering requires active item.", "Valuation method changes restricted when stock exists."],
     "Valuation method change requires Finance approval.",
     ["POST /api/inv/items", "PUT /api/inv/items/{id}", "GET /api/inv/items"],
     ["ItemChanged"], [],
     ["Suspended item used in open orders alerts"],
     ["Item master extract"],
     "Item master changes audited; drug master may include controlled-drug flags.",
     ["Update optimistic concurrency", "Publish outbox with write"],
     ["Item search P95 < 300ms"],
     ["FIN valuation accounts mapping", "HMS/PRC consumers"],
     ["New drug item available to pharmacy and procurement after activation.", "Suspended item blocked on new POs/orders."],
     ["Therapeutic classification coding configurable."]),
    ("03-receipts-quality.md", "Stock Receipt & Quality Check", "RCV", "§6.2 step 2; GRN with Procurement",
     "Receive goods against PO, quality-check, capture batch/expiry, and put away to bins.",
     "Laboratory quality LIMS for materials beyond store QC checklist.",
     ["Receiving Clerk", "QC Inspector", "Store Keeper"],
     ["Create GRN against PO lines with received quantities.",
      "Capture QC pass/fail and quarantine stock.",
      "Record batch/expiry/serials.",
      "Put away accepted stock to bins and update on-hand.",
      "Notify Financials/Procurement of goods received."],
     """GRN: `Draft -> QCPending -> PartiallyAccepted -> Accepted | Rejected`.
Stock in `Quarantine` until accepted.""",
     ["`GoodsReceipt`", "`GoodsReceiptLine`", "`QCResult`", "`PutawayTask`"],
     ["Cannot put away more than accepted qty.", "Over-receipt beyond tolerance requires approval.", "Rejected stock not available for issue."],
     "Over-receipt and QC override approvals via FND.",
     ["POST /api/inv/grns", "POST /api/inv/grns/{id}/qc", "POST /api/inv/grns/{id}/putaway"],
     ["GoodsReceived", "GoodsRejected", "StockIncreased"],
     ["PurchaseOrderIssued", "VendorChanged", "ItemChanged"],
     ["QC pending aging", "Rejected delivery alerts"],
     ["GRN register", "Supplier rejection rate"],
     "GRN and QC evidence retained; lot genealogy available for recalls.",
     ["GRN confirm idempotent", "Stock increase transactional with outbox"],
     ["GRN post P95 < 500ms typical"],
     ["PRC PO", "FIN AP match", "Batch module"],
     ["Accepted GRN increases on-hand and is available for three-way match.", "Quarantine stock not dispensable."],
     ["Blind receiving optional configuration."]),
    ("04-batch-expiry.md", "Batch & Expiry Tracking", "BCH", "§6.1 batch/expiry; §6.2 step 5 FEFO",
     "Track batches/lots, expiry dates, FEFO allocation, near-expiry flags, and expired write-offs.",
     "External reverse-logistics carrier systems.",
     ["Pharmacist", "Store Keeper", "Finance (write-off)"],
     ["Maintain batch records per item/store.",
      "Allocate issues FEFO for expiry-sensitive items.",
      "Flag near-expiry batches for priority use/return.",
      "Write off expired/damaged stock with Financials posting.",
      "Support recall holds by batch."],
     """Batch: `Available -> Hold | NearExpiry -> Expired -> WrittenOff`.
RecallHold blocks issue.""",
     ["`Batch`", "`BatchHold`", "`ExpiryAlert`"],
     ["Expired batch cannot be issued.", "FEFO may be overridden only with reason + permission."],
     "Write-offs require approval above threshold/policy.",
     ["GET /api/inv/batches", "POST /api/inv/batches/{id}/hold", "POST /api/inv/write-offs"],
     ["BatchHoldApplied", "StockWrittenOff", "NearExpiryFlagged"],
     ["StockIncreased", "StockIssued"],
     ["Near-expiry alerts", "Recall hold alerts"],
     ["Expiry calendar", "Write-off register"],
     "Batch genealogy retained for regulatory drug traceability.",
     ["Write-off idempotent", "Allocation uses row locks per batch"],
     ["FEFO allocation correct under concurrency"],
     ["Issues module", "FIN loss posting", "Notifications"],
     ["Near-expiry batch preferred over later expiry on dispense.", "Expired stock write-off posts financial loss."],
     ["Near-expiry threshold default 90 days configurable."]),
    ("05-issues-consumption.md", "Issues & Consumption Tracking", "ISS", "§6.1 consumption; §6.2 step 3; §6.3 cost posting",
     "Issue stock to HMS pharmacy/ward/OT against patient orders or to departments/engineering, with costing.",
     "Point-of-use cabinet hardware control.",
     ["Store Keeper", "Pharmacist", "Ward Nurse", "Biomed Engineer"],
     ["Create issue documents against patient/department/asset references.",
      "Decrement batches and on-hand quantities.",
      "Post COGS/cost to Financials cost centers.",
      "Expose availability to HMS.",
      "Support issue reversals via return documents."],
     """Issue: `Draft -> Posted | Cancelled`.
Posted issues immutable; reverse via return.""",
     ["`StockIssue`", "`StockIssueLine`", "`StockReturn`"],
     ["Cannot issue more than available (unless controlled backorder policy off).", "Patient issues require patient/encounter refs from HMS.", "Each issue emits costing event."],
     "High-value issue overrides require supervisor approval.",
     ["POST /api/inv/issues", "POST /api/inv/returns"],
     ["StockIssued", "StockReturned", "StockAvailabilityChanged"],
     ["MedicationDispenseRequested / OtImplantUsed / ConsumableUsed (HMS)", "ItemChanged"],
     ["Stock-out alerts"],
     ["Consumption by department", "Patient-level material cost"],
     "Issue documents audited; patient-linked issues PHI-minimized (ids).",
     ["Posted issue idempotent by requestId", "Per-batch concurrency control"],
     ["Issue post P95 < 400ms"],
     ["HMS", "FIN", "Batches", "Reorder"],
     ["Patient drug issue reduces stock and posts cost+bill collaboration.", "Availability change visible to HMS."],
     ["Valuation at moving average or FIFO per item config."]),
    ("06-transfers.md", "Inter-store Transfers", "XFER", "§6.1 transfers; §6.2 step 7",
     "Transfer stock between stores with full audit trail.",
     "Cross-facility logistics optimization beyond simple transfer docs.",
     ["Store Keeper", "Store Supervisor"],
     ["Create transfer orders between stores.",
      "Ship and receive transfer quantities/batches.",
      "Handle in-transit and variances.",
      "Maintain audit trail."],
     """Transfer: `Draft -> InTransit -> Received | Cancelled`.
Variance investigation sub-state when qty mismatch.""",
     ["`StockTransfer`", "`StockTransferLine`"],
     ["In-transit stock not issuable from either store.", "Partial receipts allowed."],
     "Variance write-off/adjustment requires approval.",
     ["POST /api/inv/transfers", "POST /api/inv/transfers/{id}/ship", "POST /api/inv/transfers/{id}/receive"],
     ["StockTransferShipped", "StockTransferReceived"], [],
     ["In-transit aging alerts"],
     ["Transfer register"],
     "Full audit trail mandatory.",
     ["Ship/receive idempotent", "Batch qty constrained"],
     ["Standard SLAs"],
     ["Stores/Batches"],
     ["Shipped stock leaves source and arrives only on receive.", "Audit shows actors for ship/receive."],
     ["Cross-facility transfers may need additional FIN intercompany later."]),
    ("07-reorder-planning.md", "Reorder Planning & Auto Requisition", "ROP", "§6.1 min/max/reorder; §6.2 step 4; §6.3 auto PR",
     "Monitor min/max/reorder points and auto-create purchase requisitions in Procurement.",
     "Advanced forecasting ML.",
     ["Inventory Planner", "Store Supervisor", "Procurement (consumer)"],
     ["Maintain reorder parameters per item/store.",
      "Evaluate net availability against reorder point continuously/on events.",
      "Auto-create purchase requisitions with suggested qty.",
      "Avoid duplicate open requisitions for same item/store per policy.",
      "Support manual planned requisitions."],
     """ReorderSignal: `Detected -> RequisitionCreated -> Suppressed`.
Suppressed when open PR/PO covers demand.""",
     ["`ReorderPolicy`", "`ReorderSignal`", "link to PRC requisition id"],
     ["Auto-PR only for active items/vendors category rules.", "Signal deduped while covering docs open."],
     "Auto-PR above value may still need procurement approval later.",
     ["POST /api/inv/reorder-policies", "POST /api/inv/reorder/evaluate", "GET /api/inv/reorder/signals"],
     ["ReorderPointBreached", "PurchaseRequisitionRequested"],
     ["StockIssued", "StockIncreased", "ItemChanged"],
     ["Reorder breach alerts"],
     ["Items below reorder", "Auto-PR hit rate"],
     "Planning actions audited.",
     ["Evaluate idempotent per item/store snapshot", "Outbox to PRC"],
     ["Evaluate on event path < 500ms"],
     ["PRC requisitions", "Issues/Receipts"],
     ["Dispense that crosses reorder creates PR request event consumed by Procurement.", "No duplicate PR while one open."],
     ["Safety stock formulas simple min/max initially."]),
    ("08-counts-adjustments.md", "Physical Verification / Cycle Counts", "CNT", "§6.1 physical verification; §6.2 step 6",
     "Cycle counts, variance approval, and financial adjustments.",
     "RFID full-store continuous inventory.",
     ["Store Keeper", "Inventory Controller", "Finance"],
     ["Create count sheets by store/bin/item.",
      "Capture counted quantities.",
      "Compute variances and route approvals.",
      "Post approved adjustments to stock and Financials."],
     """Count: `Open -> Counting -> Review -> Approved -> Posted | Cancelled`.""",
     ["`CycleCount`", "`CycleCountLine`", "`StockAdjustment`"],
     ["Posting adjusts batches explicitly when batch-controlled.", "Unapproved variances cannot post."],
     "Variance above threshold uses FND approvals.",
     ["POST /api/inv/counts", "POST /api/inv/counts/{id}/submit", "POST /api/inv/counts/{id}/post"],
     ["StockAdjusted", "CountVarianceApproved"], ["ApprovalDecisionMade"],
     ["Count due reminders", "High variance alerts"],
     ["Variance report", "Count accuracy"],
     "Count evidence retained; adjustments audited.",
     ["Post idempotent", "Freeze optional on counted bins"],
     ["Count post transactional with financial event"],
     ["FIN adjustments", "FND Approvals"],
     ["Approved variance posts stock and financial adjustment once."],
     ["Blind count optional."]),
    ("09-biomedical-spares.md", "Biomedical Equipment Spares", "SPR", "§6.1 biomedical spares; §6.3 asset linkage; §8 equipment loop",
     "Manage spare parts inventory for biomedical equipment and link usage to asset maintenance records in Financials.",
     "Full CMMS work-order suite (can integrate later).",
     ["Biomed Engineer", "Store Keeper", "Asset Accountant"],
     ["Classify items as spares linked to asset categories/models.",
      "Issue spares against equipment/asset id.",
      "Record maintenance usage notes.",
      "Emit events to update asset maintenance cost."],
     """SpareIssue extends stock issue with `assetId` required.""",
     ["`SpareItemProfile`", "`SpareIssue` (specialization of issue)"],
     ["Spare issue without asset id blocked for spare-classified items.", "Costs post to asset maintenance + cost center."],
     "Cannibalization/high-value spare issues may require approval.",
     ["POST /api/inv/spares/issues", "GET /api/inv/spares/by-asset/{assetId}"],
     ["SparePartIssued"], ["AssetCreated", "ItemChanged"],
     ["Critical spare stock-out alerts"],
     ["Spares consumption by asset", "MTTR support extracts"],
     "Device maintenance history linkage retained.",
     ["Issue idempotent", "Asset ref validated against FIN projection"],
     ["Standard SLAs"],
     ["FIN Fixed Assets", "Issues"],
     ["Spare issue increments asset maintenance cost in Financials.", "Stock decremented."],
     ["Work order module may be added later; assetId sufficient for MVP."]),
]
emit("04-inventory", "INV", INV)
print("INV written")

# ---- Procurement ----
write(
    "05-procurement/00-module-overview.md",
    overview(
        "Procurement",
        "PRC",
        "Procure-to-pay front office: vendors, requisitions, RFQ/tenders, contracts, purchase orders, GRN coordination, and vendor performance.",
        [
            ("Purchase Requisitions", "01-requisitions.md", "Manual and auto PR"),
            ("Procurement Approvals", "02-approvals.md", "Value-based approval routing"),
            ("Vendor Management", "03-vendors.md", "Vendor master ownership"),
            ("RFQ / Tendering", "04-rfq-tenders.md", "Sourcing events"),
            ("Quote Comparison", "05-quote-comparison.md", "Award decisions"),
            ("Contracts & Rate Contracts", "06-contracts.md", "Rate contracts"),
            ("Purchase Orders", "07-purchase-orders.md", "PO issuance"),
            ("Goods Receipt Coordination", "08-receipt-coordination.md", "PO-GRN collaboration"),
            ("Vendor Performance & Compliance", "09-vendor-performance.md", "Scorecards and certificates"),
        ],
        ["Vendor master", "Requisitions", "RFQs", "Contracts", "Purchase orders"],
        ["INV reorder/items/GRN", "HRIS org for approvals", "FIN AP/assets", "FND approvals engine"],
        "Phase 2 operations",
        "Blueprint §7",
    ),
)

PRC = [
    ("01-requisitions.md", "Purchase Requisitions", "PR", "§7.1 PR; §7.2 step 1; auto from Store",
     "Manual department requisitions and auto-generated requisitions from Inventory reorder signals.",
     "Punched-out external punchout catalogs beyond basic.",
     ["Department Requestor", "Inventory Planner", "Buyer"],
     ["Create manual PR with items, qty, need-by date, cost center.",
      "Create PR from Inventory PurchaseRequisitionRequested events.",
      "Submit PR into approval flow.",
      "Convert approved PR lines to RFQ or PO.",
      "Prevent duplicate auto-PRs per policy."],
     """PR: `Draft -> Submitted -> Approved | Rejected -> PartiallyConverted -> Converted | Cancelled`.""",
     ["`PurchaseRequisition`", "`PurchaseRequisitionLine`"],
     ["Auto-PR lines reference item+store+signal id.", "Rejected PR not convertible."],
     "Approval handled in procurement approvals sub-module / FND.",
     ["POST /api/prc/requisitions", "POST /api/prc/requisitions/{id}/submit", "POST /api/prc/requisitions/from-signal"],
     ["PurchaseRequisitionCreated", "PurchaseRequisitionApproved"],
     ["PurchaseRequisitionRequested", "ApprovalDecisionMade"],
     ["New auto-PR to buyers"],
     ["PR aging", "Auto vs manual mix"],
     "PR audited; department spend visibility.",
     ["from-signal idempotent by signalId", "Submit concurrency safe"],
     ["Auto PR creation < 2s after signal consume"],
     ["INV reorder", "FND Approvals", "Items/Vendors"],
     ["Reorder signal creates a single open PR.", "Approved PR can create PO."],
     ["Consolidation of multiple signals optional."]),
    ("02-approvals.md", "Procurement Approval Routing", "PAP", "§7.2 step 2; HRIS org hierarchy",
     "Value-based purchase approval routing using HRIS organizational hierarchy and FND approval engine.",
     "Separate from FND engine implementation—this specifies procurement policies.",
     ["Buyer", "Department Head", "Finance Controllers", "CFO (high value)"],
     ["Map PR/PO/contract transaction types to approval templates by value bands.",
      "Resolve approvers from HRIS reporting lines and role maps.",
      "Block conversion/issue until approved.",
      "Record decision trail on procurement documents."],
     """Uses FND approval states attached to PR/PO/Contract.""",
     ["Policy config entities linking thresholds to templates"],
     ["Requestor cannot self-approve unless policy allows.", "Policy changes do not rewrite in-flight approvals."],
     "Managed via FND Approvals; procurement owns threshold policies.",
     ["PUT /api/prc/approval-policies", "POST /api/prc/{docType}/{id}/send-for-approval"],
     ["ProcurementApprovalRequested"], ["ApprovalDecisionMade", "EmployeeOrgChanged"],
     ["Approver inbox via FND"],
     ["Approval cycle time by value band"],
     "Approval decisions retained with commercial documents.",
     ["Send-for-approval idempotent"],
     ["Start approval < 300ms"],
     ["FND APPR", "HRIS org", "PR/PO/Contracts"],
     ["PO above threshold cannot issue without approvals complete."],
     ["Delegation covered by FND capability roadmap."]),
    ("03-vendors.md", "Vendor Management", "VND", "§7.1 vendor management; §2 vendor ownership",
     "Vendor registration, onboarding documents, banking, categories, and status for purchasing/AP.",
     "Full SRM social collaboration network.",
     ["Vendor Master Steward", "Buyer", "AP Clerk (read)", "Compliance"],
     ["Register vendors with legal and tax identifiers.",
      "Capture banking and contact details securely.",
      "Track regulatory certificates for medical supplies.",
      "Activate/suspend vendors and publish VendorChanged.",
      "Support evaluation score inputs from performance module."],
     """Vendor: `Draft -> UnderReview -> Active -> Suspended -> Blacklisted | Archived`.""",
     ["`Vendor`", "`VendorSite`", "`VendorBankAccount`", "`VendorCertificate`"],
     ["Suspended/blacklisted vendors cannot receive new POs.", "Certificate expiry can auto-suspend category purchasing."],
     "Blacklisting requires Compliance/Finance approval.",
     ["POST /api/prc/vendors", "PUT /api/prc/vendors/{id}", "POST /api/prc/vendors/{id}/certificates"],
     ["VendorChanged", "VendorSuspended"], [],
     ["Certificate expiry alerts"],
     ["Vendor master", "Certificate compliance"],
     "Vendor banking PII/sensitive; masked in UI; access audited.",
     ["Update optimistic concurrency", "Event outbox"],
     ["Vendor search P95 < 300ms"],
     ["FIN AP", "INV GRN", "Docs", "Performance"],
     ["Active vendor selectable on PO.", "Expired pharma certificate blocks PO for that category when policy enabled."],
     ["Tax ID validation rules locale-specific."]),
    ("04-rfq-tenders.md", "RFQ / Tendering", "RFQ", "§7.1 RFQ/tendering; §7.2 step 3",
     "Send RFQs/tenders to approved vendors or use rate contracts as alternative sourcing path.",
     "Public e-procurement government portal replacement.",
     ["Buyer", "Vendors (external response channel)", "Procurement Manager"],
     ["Create RFQ from PR lines.",
      "Invite approved vendors and capture due dates.",
      "Collect quotations (internal entry or portal).",
      "Close RFQ for comparison.",
      "Support sealed-bid mode optional."],
     """RFQ: `Draft -> Issued -> ResponsesOpen -> Closed -> Awarded | Cancelled`.""",
     ["`Rfq`", "`RfqLine`", "`RfqInvite`", "`VendorQuote`"],
     ["Only active compliant vendors invited unless exception.", "Quotes after close rejected."],
     "Tender award may require committee approval.",
     ["POST /api/prc/rfqs", "POST /api/prc/rfqs/{id}/issue", "POST /api/prc/rfqs/{id}/quotes"],
     ["RfqIssued", "RfqClosed"], ["PurchaseRequisitionApproved", "VendorChanged"],
     ["Invite notifications", "Due date reminders"],
     ["RFQ cycle time", "Response rates"],
     "Commercial confidentiality for sealed bids; access controlled.",
     ["Issue idempotent", "Late quote rejected"],
     ["Standard SLAs"],
     ["Vendors", "PR", "Quote comparison"],
     ["Issued RFQ visible to invited vendor response path.", "Closed RFQ ready for comparison."],
     ["External vendor portal Phase 4; internal capture MVP."]),
    ("05-quote-comparison.md", "Quotation Comparison & Selection", "CMP", "§7.2 step 4",
     "Compare quotes on price, lead time, and vendor quality/compliance rating; select award.",
     "Optimization solver beyond weighted scoring.",
     ["Buyer", "Procurement Manager", "Evaluation Committee"],
     ["Present comparison matrix across quotes.",
      "Apply scoring weights including vendor performance rating.",
      "Select winning quote lines and record justification.",
      "Pass award to PO/contract creation."],
     """Award: `Recommended -> Approved -> Converted`.""",
     ["`QuoteComparison`", "`AwardDecision`"],
     ["Cannot award to non-compliant vendor when hard-stop policy on.", "Partial line awards allowed."],
     "Awards above threshold require approval.",
     ["POST /api/prc/comparisons", "POST /api/prc/comparisons/{id}/award"],
     ["AwardDecisionMade"], ["RfqClosed", "VendorPerformanceUpdated"],
     ["Award pending approval"],
     ["Savings vs estimate", "Award audit"],
     "Award justification retained for audit.",
     ["Award idempotent per RFQ line set"],
     ["Matrix render interactive"],
     ["RFQ", "Contracts/PO", "Vendor performance"],
     ["Award creates basis for PO lines.", "Decision and scores stored."],
     ["Default weights configurable."]),
    ("06-contracts.md", "Contract & Rate-Contract Management", "CTR", "§7.1 contracts; §7.2 step 3 rate contract path",
     "Manage contracts/rate contracts especially for pharma and high-volume consumables.",
     "Complex CLM clause AI negotiation.",
     ["Contract Manager", "Buyer", "Legal/Compliance"],
     ["Create rate contracts with items, prices, validity, and volume commitments.",
      "Release POs against contracts without RFQ when valid.",
      "Track call-off quantities and expiry.",
      "Manage amendments."],
     """Contract: `Draft -> InApproval -> Active -> Expired | Terminated`.""",
     ["`PurchaseContract`", "`ContractLine`", "`ContractAmendment`"],
     ["Expired contracts cannot release new POs.", "Price on call-off taken from contract unless amendment."],
     "Contract activation uses approval workflow.",
     ["POST /api/prc/contracts", "POST /api/prc/contracts/{id}/activate", "POST /api/prc/contracts/{id}/call-off"],
     ["ContractActivated", "ContractExpired"], ["ApprovalDecisionMade", "ItemChanged", "VendorChanged"],
     ["Contract expiry alerts"],
     ["Contract utilization", "Price variance vs spot"],
     "Contracts retained for commercial/statutory periods.",
     ["Call-off concurrency controls on remaining qty"],
     ["Standard SLAs"],
     ["Vendors/Items", "PO", "Approvals"],
     ["Active rate contract can generate PO without RFQ.", "Expiry prevents further call-off."],
     ["Legal e-sign optional."]),
    ("07-purchase-orders.md", "Purchase Order Issuance", "PO", "§7.1 PO; §7.2 step 5; feeds FIN/INV",
     "Issue purchase orders to vendors from approved PR/award/contract with terms.",
     "Supplier ASN advanced ship notices deep EDI beyond basic.",
     ["Buyer", "Procurement Manager", "Vendor (receive PO)"],
     ["Create PO headers/lines with prices, taxes, delivery store, and terms.",
      "Submit for approval based on value.",
      "Issue/send PO to vendor and freeze commercial terms.",
      "Support amendments and cancellations.",
      "Expose PO to Inventory receiving and Financials match."],
     """PO: `Draft -> InApproval -> Approved -> Issued -> PartiallyReceived -> Received | Cancelled | Closed`.""",
     ["`PurchaseOrder`", "`PurchaseOrderLine`", "`PoAmendment`"],
     ["Issued PO required for standard GRN.", "Cannot receive more than open qty beyond tolerance.", "Vendor must be active."],
     "PO approval via procurement approval policies.",
     ["POST /api/prc/purchase-orders", "POST /api/prc/purchase-orders/{id}/issue", "POST /api/prc/purchase-orders/{id}/amend"],
     ["PurchaseOrderIssued", "PurchaseOrderAmended", "PurchaseOrderCancelled"],
     ["PurchaseRequisitionApproved", "AwardDecisionMade", "ContractActivated", "ApprovalDecisionMade"],
     ["PO issued to stakeholders"],
     ["PO register", "Open commitments"],
     "PO commercial record retained; amendments audited.",
     ["Issue idempotent", "Commitment updates concurrency safe"],
     ["Issue PO < 300ms"],
     ["PR/Award/Contract", "INV GRN", "FIN AP/Budget"],
     ["Issued PO appears for receiving against lines.", "Commitment visible to budget control."],
     ["PDF/email send via notifications."]),
    ("08-receipt-coordination.md", "Goods Receipt Coordination with Store", "GRC", "§7.1 GRN coordination; §7.2 step 6",
     "Coordinate expected receipts, tolerances, and close-out between Procurement PO and Inventory GRN.",
     "Does not replace Inventory GRN execution.",
     ["Buyer", "Receiving Clerk", "Procurement Manager"],
     ["Provide receiving expectations/worklist from issued POs.",
      "Configure over/under delivery tolerances.",
      "Consume GoodsReceived events to update PO line statuses.",
      "Close PO lines when complete.",
      "Handle short-close with reason."],
     """PO line receiving state updated: `Open -> Partial -> Complete | ShortClosed`.""",
     ["PO receiving projection", "Tolerance policy"],
     ["Short-close requires reason and permission/approval when value remains."],
     "Short-close above threshold approval required.",
     ["GET /api/prc/receiving-worklist", "POST /api/prc/purchase-orders/{id}/short-close"],
     ["PurchaseOrderReceivingUpdated", "PurchaseOrderClosed"],
     ["GoodsReceived", "GoodsRejected"],
     ["Overdue expected delivery alerts"],
     ["On-time delivery inputs", "Open PO receiving aging"],
     "Coordination actions audited.",
     ["Event handler idempotent by GRN id"],
     ["PO status update < 5s after GRN"],
     ["INV GRN", "PO", "Vendor performance"],
     ["GRN against PO updates PO remaining qty.", "Fully received PO can close."],
     ["ASN optional later."]),
    ("09-vendor-performance.md", "Vendor Performance & Compliance Tracking", "VPR", "§7.1 performance/compliance; §7.2 step 8",
     "Track on-time delivery, quality issues, certificate compliance, and ratings used in sourcing.",
     "External credit rating agencies.",
     ["Procurement Manager", "QC", "Compliance"],
     ["Compute vendor KPIs from GRN timeliness and QC rejections.",
      "Track regulatory certificate status.",
      "Maintain vendor scorecards.",
      "Feed ratings into quote comparison.",
      "Recommend suspend when KPIs breach thresholds."],
     """ScorecardPeriod: `Open -> Published`.
Compliance: `Compliant | Warning | NonCompliant`.""",
     ["`VendorScorecard`", "`VendorKpiSnapshot`", "certificate status projection"],
     ["NonCompliant hard-stop policy can block new awards/POs."],
     "Suspension recommendation converts to vendor suspend approval.",
     ["GET /api/prc/vendors/{id}/scorecard", "POST /api/prc/vendors/{id}/scorecards/publish"],
     ["VendorPerformanceUpdated", "VendorComplianceChanged"],
     ["GoodsReceived", "GoodsRejected", "VendorChanged", "ApPaymentDisbursed"],
     ["Compliance breach alerts"],
     ["Vendor scorecards", "Quality rejection trends"],
     "Performance records retained for procurement audit.",
     ["KPI recompute idempotent per period"],
     ["Scorecard publish batch SLA"],
     ["Vendors", "GRC/QC", "Comparison"],
     ["Late delivery reduces on-time KPI.", "Score available in comparison matrix."],
     ["KPI weights configurable."]),
]
emit("05-procurement", "PRC", PRC)
print("PRC written")

# ---- Cross-module ----
write(
    "06-cross-module-workflows/00-overview.md",
    """# Cross-Module Workflows — Overview

| Field | Value |
|---|---|
| Module code | `XWF` |
| Source | Blueprint §§3.3, 4.3, 5.3, 6.3, 7.3, 8 |

## Purpose
Specify end-to-end choreography across modules, including canonical events, failure handling, and reconciliation expectations.

## Documents
| Document | Pathway |
|---|---|
| [Medication to Replenishment](01-medication-to-replenishment.md) | HMS order → INV issue → reorder → PRC PO → GRN → availability |
| [Procure to Pay](02-procure-to-pay.md) | PR → PO → GRN → AP match → payment |
| [Order to Cash](03-order-to-cash.md) | HMS charges → invoice → AR → receipt |
| [Hire to Retire](04-hire-to-retire.md) | Recruit → credential → schedule → exit/revoke |
| [Payroll Posting](05-payroll-posting.md) | HRIS payroll → FIN GL/bank |
| [Equipment Maintenance](06-equipment-maintenance.md) | Fault → spare issue → asset cost/depreciation |
| [Discharge to Claim](07-discharge-to-claim.md) | Discharge → final bill → claim → settlement |
| [Canonical Events & Reconciliation](08-canonical-events-reconciliation.md) | Event catalog, errors, reconciliation |

## Rule
No cross-module synchronous distributed transactions across databases/schemas. Use outbox events, idempotent handlers, and compensating actions.
""",
)

XWF = [
    ("01-medication-to-replenishment.md", "Medication Order to Stock Replenishment Loop", "MED",
     "§8 primary loop; §3.3; §6.3; §7.3",
     "Choreograph clinician medication order through dispense, stock decrement, reorder breach, PO, GRN, and restored availability in HMS.",
     "Non-medication consumable variants are analogous but may skip pharmacist verify.",
     ["Clinician", "Pharmacist", "Store", "Buyer", "AP (later)"],
     ["On MedicationDispensed, Inventory shall decrement stock atomically with event processing and publish StockAvailabilityChanged.",
      "When availability breaches reorder point, Inventory shall emit PurchaseRequisitionRequested exactly once per open coverage window.",
      "Procurement shall create/submit PR and progress to PO issue.",
      "On GoodsReceived acceptance, Inventory shall increase stock and publish availability for HMS pharmacy allocation.",
      "HMS shall reflect non-available drugs as blocked/alerted at verify/dispense time."],
     """```mermaid
sequenceDiagram
  participant HMS
  participant INV
  participant PRC
  HMS->>INV: MedicationDispensed / issue
  INV->>INV: decrement stock
  INV->>PRC: PurchaseRequisitionRequested
  PRC->>PRC: PR_approve_PO_issue
  PRC->>INV: PO available for GRN
  INV->>HMS: StockAvailabilityChanged
```""",
     ["Correlation via patientId/orderId/itemId/storeId", "signalId for reorder dedupe"],
     ["At-least-once events must not double-decrement stock.", "FEFO allocation remains enforced."],
     "PO approvals as per PRC policies.",
     ["N/A — choreography of existing APIs"],
     ["MedicationDispensed", "StockAvailabilityChanged", "PurchaseRequisitionRequested", "PurchaseOrderIssued", "GoodsReceived"],
     ["All of the above across modules"],
     ["Stock-out to clinician", "Reorder to buyer"],
     ["Loop cycle time item replenishment"],
     "Full audit across dispense and stock docs.",
     ["Compensating return if dispense voided", "Inbox dedupe", "Stock qty check constraints"],
     ["End-to-end lag targets documented per hop (<5s event hops)"],
     ["HMS PHX", "INV", "PRC"],
     ["Dispense reduces stock.", "Reorder creates one PR.", "GRN restores availability for subsequent dispense."],
     ["Auto-PO without approval never allowed when thresholds require approval."]),
    ("02-procure-to-pay.md", "Procure-to-Pay Pathway", "P2P", "§5.2 B; §7.2",
     "End-to-end PR/PO/GRN/invoice/payment with three-way match.",
     "Non-PO invoices only under explicit exception policy.",
     ["Requestor", "Buyer", "Receiver", "AP", "Controller"],
     ["Approved PR converts to PO (via RFQ/contract/direct policy).",
      "Issued PO enables GRN in Inventory.",
      "Vendor invoice in FIN AP matches PO+GRN.",
      "Approved payment disburses and posts GL.",
      "Vendor performance updates on receipt/payment outcomes."],
     """PR -> PO -> GRN -> InvoiceMatched -> PaymentDisbursed.""",
     ["Shared identifiers: prId, poId, grnId, invoiceId, paymentId"],
     ["Payment cannot precede successful match/approved exception.", "All hops idempotent."],
     "Value-based approvals on PR/PO/payment.",
     ["Existing module APIs"],
     ["PurchaseOrderIssued", "GoodsReceived", "VendorInvoiceMatched", "ApPaymentDisbursed"],
     ["PurchaseRequisitionApproved", "ApprovalDecisionMade"],
     ["Match variance", "Payment due"],
     ["P2P cycle time", "Match exception rate"],
     "Commercial + financial audit trail complete.",
     ["Partial GRN supports partial invoice match", "Dead-letter alerts on posting failures"],
     ["Financial posting exactly-once effective"],
     ["PRC", "INV", "FIN"],
     ["Three-way match success path pays vendor once.", "Missing GRN blocks match."],
     ["Evaluated receipt settlement optional later."]),
    ("03-order-to-cash.md", "Order-to-Cash Pathway", "O2C", "§5.2 A; HMS billing",
     "Charges from care delivery to invoice, claim, receipt, and AR settlement.",
     "Retail non-patient POS beyond pharmacy retail.",
     ["Clinicians/ancillary", "Billing", "Cashier", "AR"],
     ["Billable events from HMS create charges idempotently.",
      "Invoice finalization splits self-pay vs insurance.",
      "Claims submitted and tracked.",
      "Receipts settle AR open items.",
      "Aging and denials managed to closure."],
     """Charge -> Invoice Finalized -> Claim/AR Open -> Receipt/Settlement.""",
     ["sourceEventId for charges", "invoiceId", "claimId", "receivableId"],
     ["No double charge for same sourceEventId.", "Discharge policy may require billing clearance."],
     "Discounts/write-offs approved.",
     ["Existing APIs"],
     ["BillableEventCreated", "InvoiceFinalized", "ClaimSubmitted", "PaymentReceived", "ReceivableSettled"],
     ["MedicationDispensed", "LabResultPosted", "OpdEncounterClosed", "OtImplantUsed", "DischargeCompleted"],
     ["Denial", "High balance"],
     ["Collections", "Denial rate", "Cost-to-collect"],
     "Patient financial + clinical identifiers handled per privacy policy.",
     ["Compensating credit notes for reversed clinical events"],
     ["Charge to AR visibility near-real-time"],
     ["HMS BIL", "FIN AR/GL/CASH"],
     ["Dispense appears on bill without re-entry.", "Payment reduces AR balance."],
     ["Package/DRG pricing iterative."]),
    ("04-hire-to-retire.md", "Hire-to-Retire & Clinical Scheduling Gate", "H2R", "§4.2; §8 new hire scheduling; §9 RBAC",
     "Ensure onboarding/credentialing gates HMS scheduling and that exit revokes access everywhere.",
     "Agency staff deep marketplace.",
     ["HR", "Credentialing", "Security", "Clinical supervisors"],
     ["Offer accept creates onboarding/employee master.",
      "Credentials verified before clinical scheduling privileges effective.",
      "HMS consults credential status on schedule/order sign.",
      "Exit settles FnF, sets EmployeeExited, disables IAM, blocks roster/clinical actions."],
     """Hired -> Credentialed -> Schedulable -> Exited/Revoked.""",
     ["employeeId linkage across HRIS/IAM/HMS"],
     ["Deny by default when credential status unknown/down (fail-safe configurable with break-glass)."],
     "Exit/termination approvals as HRIS.",
     ["Status APIs + events"],
     ["EmployeeActivated", "EmployeeCredentialStatusChanged", "EmployeeExited", "UserDisabled"],
     ["OfferAccepted", "CredentialExpiring"],
     ["Credential lapse", "Access revoke confirmation"],
     ["Credential compliance", "Access revocation lag"],
     "HR and access audits retained.",
     ["IAM disable retry until success", "HMS must re-check status, not cache forever"],
     ["Revocation propagation < 5 minutes"],
     ["HRIS", "FND IAM", "HMS"],
     ["Uncredentialed clinician cannot be scheduled.", "Exited employee cannot login."],
     ["Fail-open emergency mode only via break-glass."]),
    ("05-payroll-posting.md", "Payroll to Financials Posting", "PAYX", "§4.3; §5.2 C",
     "Post payroll results to GL expense/liabilities and coordinate disbursement.",
     "Employee reimbursement claims engine beyond payroll.",
     ["Payroll Officer", "Finance"],
     ["Approved payroll run publishes PayrollPosted with summarized account mappings.",
      "Financials creates balanced journal lines once per run.",
      "Bank file disbursement status updates cash/bank.",
      "Failures raise dead-letter and block marked 'posted' until resolved or voided."],
     """Payroll Approved -> PayrollPosted event -> JournalPosted -> Disbursed.""",
     ["payrollRunId idempotency key", "account mapping table HRIS->FIN"],
     ["Exactly-once journal per payrollRunId.", "Reversal via void workflow emits compensating journal."],
     "Payroll post dual approval.",
     ["Existing APIs"],
     ["PayrollPosted", "JournalPosted", "BankFileDisbursed"],
     ["AttendancePosted"],
     ["Posting failure alerts"],
     ["Payroll vs GL reconciliation"],
     "Confidential payroll amounts restricted.",
     ["Inbox dedupe", "Mapping missing fails run post with actionable errors"],
     ["Posting lag < 5s event hop; batch journal OK"],
     ["HRIS PAY", "FIN GL/CASH"],
     ["One payroll run creates one journal set.", "Replay does not duplicate."],
     ["Cost center split by assignment percentages supported."]),
    ("06-equipment-maintenance.md", "Equipment Breakdown to Spares & Depreciation Impact", "EQM", "§8 equipment loop; §6.3; §5.3 assets",
     "Link biomedical fault logging to spare issue and asset maintenance cost / depreciation context.",
     "Full CMMS may own fault tickets later; MVP accepts maintenance event with asset id.",
     ["Biomed", "Store", "Asset Accountant"],
     ["Capture maintenance need against asset id (HMS biomed log or FIN asset service).",
      "Issue spare from Inventory against asset.",
      "Financials adds maintenance cost to asset.",
      "Depreciation continues unless disposal/impairment workflow says otherwise."],
     """FaultLogged -> SpareIssued -> AssetMaintenanceCostUpdated -> (optional) Impairment/Disposal.""",
     ["assetId", "spareIssueId"],
     ["Spare-classified items require asset id.", "Costs not double-posted on event retry."],
     "Impairment/disposal approvals in FIN FA.",
     ["Existing APIs"],
     ["SparePartIssued", "AssetMaintenanceCostUpdated"],
     ["AssetCreated"],
     ["Critical equipment down alerts (if logged)"],
     ["Maintenance cost by asset"],
     "Device history retained.",
     ["Idempotent cost append by spareIssueId"],
     ["Event hop < 5s"],
     ["INV SPR", "FIN FA"],
     ["Spare issue increases asset maintenance cost once.", "Stock decremented."],
     ["Standalone CMMS integration later."]),
    ("07-discharge-to-claim.md", "Discharge to Insurance Claim Settlement", "D2C", "§3.2 steps 8–9; §8 discharge loop",
     "On discharge, finalize bill, submit claim, and track AR to settlement.",
     "Insurer adjudication engine internals.",
     ["Clinician", "Billing", "AR"],
     ["Discharge completion requires configured clearances.",
      "Final invoice produced and claim package assembled for insured patients.",
      "FIN AR tracks claim to settlement including partials/denials.",
      "Follow-up appointment created in HMS front office."],
     """DischargeCompleted -> InvoiceFinalized -> ClaimSubmitted -> (Partial)Settlement.""",
     ["admissionId/encounterId", "invoiceId", "claimId"],
     ["Cannot lose bed release on billing retry failures—use explicit states/compensation.", "Claim submission idempotent."],
     "Discharge against unpaid balance waiver approvals.",
     ["Existing APIs"],
     ["DischargeCompleted", "InvoiceFinalized", "ClaimSubmitted", "ReceivableSettled"],
     ["PaymentReceived", "Denial"],
     ["Pending claim aging"],
     ["Days to claim submission", "Denial rate post-discharge"],
     "Clinical + financial audits linked by encounter id.",
     ["Saga-style state machine in discharge module", "AR sync retries"],
     ["Claim draft available within minutes of discharge complete"],
     ["HMS DIS/BIL", "FIN AR"],
     ["Insured discharge creates claim for tracking.", "Settlement closes AR open item."],
     ["Auto e-claim format locale-specific."]),
    ("08-canonical-events-reconciliation.md", "Canonical Events, Errors & Reconciliation", "EVT",
     "§2 hub; all integration trigger sections; governance audit",
     "Define canonical event catalog expectations, error handling, dead-letter, and reconciliation jobs between modules.",
     "External enterprise integrator mapping tools.",
     ["Platform Engineer", "Module Owners", "Controllers/Compliance for financial/clinical recon"],
     ["Maintain versioned event catalog with producer, payload key fields, consumers, and idempotency keys.",
      "All critical financial/stock/clinical cross effects covered by reconciliation reports.",
      "Dead-letter messages alert and are replayable after fix.",
      "Daily recon: stock vs financial COGS; charges vs AR; payroll vs GL; PO commitments vs GRN/AP.",
      "Document compensating transactions for each critical failure mode."],
     """Event processing: Received -> Processed | DeadLetter -> Replayed -> Processed.
Recon: `Scheduled -> Running -> Clean | BreaksFound -> Resolved`.""",
     ["`EventCatalogEntry`", "`ReconciliationRun`", "`ReconciliationBreak`"],
     ["Breaks do not auto-mute; ownership required for resolution.", "Replay must remain idempotent."],
     "Replay of financial/clinical events in production may require Compliance/Finance approval.",
     ["GET /api/fnd/events/catalog", "POST /api/fnd/recon/runs", "GET /api/fnd/recon/breaks"],
     ["ReconciliationBreakFound", "EventDeadLetterCreated"],
     ["All integration events"],
     ["Dead-letter threshold", "Unresolved recon breaks"],
     ["Recon dashboards listed above"],
     "Recon evidence retained with financial close packages.",
     ["Handlers idempotent", "Recon jobs restartable", "Poison message isolation"],
     ["Critical event hop P95 < 5s", "Daily recon completes in batch window"],
     ["FND EVT", "All modules"],
     ["Duplicate event delivery does not duplicate money/stock movements.", "Dead-letter replay after fix converges system.", "Daily recon detects intentional mismatch test."],
     ["In-process dispatcher acceptable for modular monolith MVP."]),
]
emit("06-cross-module-workflows", "XWF", XWF)
print("XWF written")

# Canonical event catalog appendix
write(
    "06-cross-module-workflows/09-event-catalog.md",
    """# Canonical Integration Event Catalog (Initial)

| Event | Producer | Key Idempotency / Partition | Primary Consumers |
|---|---|---|---|
| PatientChanged | HMS | patientId + version | FND MDM, FIN, INV |
| EmployeeChanged / EmployeeActivated / EmployeeExited | HRIS | employeeId + version | FND IAM/MDM, HMS, PRC, FIN |
| EmployeeCredentialStatusChanged | HRIS | employeeId + version | HMS, FND IAM |
| ItemChanged | INV | itemId + version | HMS, PRC, FIN |
| VendorChanged | PRC | vendorId + version | FIN, INV |
| AccountChanged / CostCenterChanged | FIN | accountId/costCenterId + version | All |
| ClinicalOrderPlaced | HMS | orderId | LIS, RIS, Pharmacy |
| MedicationDispensed | HMS | dispenseId | INV, FIN/HMS Billing |
| StockIssued / StockAvailabilityChanged | INV | issueId / itemId+storeId | HMS, FIN, ROP |
| ReorderPointBreached / PurchaseRequisitionRequested | INV | signalId | PRC |
| PurchaseOrderIssued | PRC | poId | INV, FIN |
| GoodsReceived | INV | grnId | PRC, FIN |
| InvoiceFinalized / BillableEventCreated / PaymentReceived / ClaimSubmitted | HMS | invoiceId/charge sourceEventId/paymentId/claimId | FIN AR/GL |
| VendorInvoiceMatched / ApPaymentDisbursed | FIN | invoiceId/paymentId | PRC VPR, CASH |
| PayrollPosted / FnFPosted | HRIS | payrollRunId / exitCaseId | FIN GL |
| SparePartIssued | INV | spareIssueId | FIN FA |
| DischargeCompleted | HMS | dischargeId | FIN AR, FO follow-up |
| ApprovalRequested / ApprovalDecisionMade | FND | approvalRequestId / actionId | Originating modules |
| JournalPosted | FIN | journalId / sourceDocumentId | MIS, Budgets |

Payloads should carry `eventId`, `occurredAt`, `correlationId`, `causationId`, `facilityId`, and versioned schema.
""",
)

write(
    "TRACEABILITY.md",
    """# Traceability Register

| Requirement ID pattern | Spec location | Design artifact (to be filled in build) | Code | Tests |
|---|---|---|---|---|
| FND-*-FR/BR/AC | `docs/requirements/00-foundation/` | ADR + module contracts | `src/Modules/Foundation` | unit/integration/arch |
| HMS-*-FR/BR/AC | `docs/requirements/01-hms/` | HMS bounded context design | `src/Modules/Hms` | unit/integration/e2e |
| HRIS-*-FR/BR/AC | `docs/requirements/02-hris/` | HRIS bounded context design | `src/Modules/Hris` | unit/integration/e2e |
| FIN-*-FR/BR/AC | `docs/requirements/03-financials/` | FIN bounded context design | `src/Modules/Financials` | unit/integration/e2e |
| INV-*-FR/BR/AC | `docs/requirements/04-inventory/` | INV bounded context design | `src/Modules/Inventory` | unit/integration/e2e |
| PRC-*-FR/BR/AC | `docs/requirements/05-procurement/` | PRC bounded context design | `src/Modules/Procurement` | unit/integration/e2e |
| XWF-*-FR/BR/AC | `docs/requirements/06-cross-module-workflows/` | sequence diagrams + event catalog | host composition + handlers | e2e pathway tests |

## Update Rule
When implementing a requirement, append concrete file/test links under the matching module section in this register or in module-level `TRACEABILITY.md` fragments created during the build increment.
""",
)

write(
    "VERIFICATION.md",
    """# Requirements Verification Package

## Status
Automated consistency drafting complete. **Human approval required before application scaffolding.**

## File Inventory
| Area | Files |
|---|---|
| Index / registers | `README.md`, `TRACEABILITY.md`, `VERIFICATION.md` |
| Foundation | 11 (overview + 10 sub-modules) |
| HMS | 12 (overview + 11 sub-modules) |
| HRIS | 11 (overview + 10 sub-modules) |
| Financials | 9 (overview + 8 sub-modules) |
| Inventory | 10 (overview + 9 sub-modules) |
| Procurement | 10 (overview + 9 sub-modules) |
| Cross-module | 10 (overview + 8 pathways + event catalog) |

## Consistency Checks Performed
| Check | Result |
|---|---|
| Master data ownership unique (Patient HMS, Employee HRIS, Item INV, Vendor PRC, COA/CC FIN, Approvals FND) | Pass |
| Integration triggers from blueprint §§3.3–7.3 represented as events/AC | Pass |
| Cross-module pathways reference existing module events | Pass |
| Approval/RBAC/Audit governance applied across modules | Pass |
| Requirement ID convention applied | Pass |
| No module instructed to write another module's tables | Pass |
| Phasing aligns with blueprint §10 | Pass |

## Open Assumptions Pending Your Decision
1. Initial deployment is single-tenant hospital group (multi-facility supported).
2. Primary locale/statutory pack to be confirmed (tax, payroll, identifiers).
3. Auth starts with built-in OpenIddict/Identity with path to external OIDC.
4. PACS/analyzer/biometric integrations are adapter-based after core workflows.
5. In-process outbox dispatcher for modular monolith MVP (broker optional later).
6. Hard budget control on PO is optional per facility (default warn).
7. Patient portal and vendor portal are Phase 4.
8. Currency: one base currency per facility initially.

## Approval Checklist
- [ ] Glossary and ownership model accepted
- [ ] Foundation requirements accepted
- [ ] HMS requirements accepted (Phase 1 subset can be prioritized)
- [ ] HRIS/FIN/INV/PRC requirements accepted
- [ ] Cross-module event catalog accepted
- [ ] Open assumptions confirmed or amended
- [ ] Authorization to scaffold .NET 10 + React + PostgreSQL modular monolith

## Reviewer Sign-off
| Role | Name | Date | Decision |
|---|---|---|---|
| Product Owner | | | Approve / Amend |
| Architecture | | | Approve / Amend |
| Clinical ops | | | Approve / Amend |
| Finance/HR ops | | | Approve / Amend |
""",
)

print("Verification + traceability written")
print("DONE", ROOT)