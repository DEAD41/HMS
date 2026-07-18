namespace HealthcareERP.Modules.Procurement.Contracts.Events;

public sealed record PurchaseOrderIssued(Guid PurchaseOrderId, Guid VendorId, Guid FacilityId, decimal TotalAmount);
