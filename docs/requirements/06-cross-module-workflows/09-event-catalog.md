# Canonical Integration Event Catalog (Initial)

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
