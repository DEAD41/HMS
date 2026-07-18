using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Procurement.Domain;

public sealed class PurchaseRequisition : AggregateRoot
{
    private PurchaseRequisition() { }

    public Guid FacilityId { get; private set; }
    public Guid? ItemId { get; private set; }
    public Guid? StoreId { get; private set; }
    public Guid? SignalId { get; private set; }
    public string Description { get; private set; } = string.Empty;
    public decimal Quantity { get; private set; }
    public string Status { get; private set; } = "Draft";

    public static Result<PurchaseRequisition> Create(
        Guid facilityId,
        string description,
        decimal quantity,
        Guid? itemId,
        Guid? storeId,
        Guid? signalId)
    {
        if (quantity <= 0) return Result.Failure<PurchaseRequisition>("Quantity must be positive.");
        return Result.Success(new PurchaseRequisition
        {
            FacilityId = facilityId,
            Description = description.Trim(),
            Quantity = quantity,
            ItemId = itemId,
            StoreId = storeId,
            SignalId = signalId,
            Status = "Approved"
        });
    }
}
