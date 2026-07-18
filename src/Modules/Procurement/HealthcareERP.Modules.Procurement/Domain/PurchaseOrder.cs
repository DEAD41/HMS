using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Procurement.Domain;

public sealed class PurchaseOrder : AggregateRoot
{
    private PurchaseOrder() { }

    public Guid FacilityId { get; private set; }
    public Guid VendorId { get; private set; }
    public Guid? RequisitionId { get; private set; }
    public Guid? ItemId { get; private set; }
    public decimal Quantity { get; private set; }
    public decimal UnitPrice { get; private set; }
    public string Currency { get; private set; } = "USD";
    public string Status { get; private set; } = "Draft";

    public decimal TotalAmount => Quantity * UnitPrice;

    public static Result<PurchaseOrder> Issue(
        Guid facilityId,
        Guid vendorId,
        decimal quantity,
        decimal unitPrice,
        string currency,
        Guid? requisitionId,
        Guid? itemId)
    {
        if (quantity <= 0) return Result.Failure<PurchaseOrder>("Quantity must be positive.");
        if (unitPrice < 0) return Result.Failure<PurchaseOrder>("Unit price cannot be negative.");
        return Result.Success(new PurchaseOrder
        {
            FacilityId = facilityId,
            VendorId = vendorId,
            Quantity = quantity,
            UnitPrice = unitPrice,
            Currency = currency.Trim().ToUpperInvariant(),
            RequisitionId = requisitionId,
            ItemId = itemId,
            Status = "Issued"
        });
    }
}
