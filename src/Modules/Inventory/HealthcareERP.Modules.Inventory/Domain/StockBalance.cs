using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Inventory.Domain;

public sealed class StockBalance : AggregateRoot
{
    private StockBalance() { }

    public Guid FacilityId { get; private set; }
    public Guid StoreId { get; private set; }
    public Guid ItemId { get; private set; }
    public decimal QuantityOnHand { get; private set; }

    public static StockBalance Create(Guid facilityId, Guid storeId, Guid itemId) => new()
    {
        FacilityId = facilityId,
        StoreId = storeId,
        ItemId = itemId,
        QuantityOnHand = 0
    };

    public Result Increase(decimal qty)
    {
        if (qty <= 0) return Result.Failure("Quantity must be positive.");
        QuantityOnHand += qty;
        Touch();
        return Result.Success();
    }

    public Result Decrease(decimal qty)
    {
        if (qty <= 0) return Result.Failure("Quantity must be positive.");
        if (qty > QuantityOnHand) return Result.Failure("Insufficient stock.");
        QuantityOnHand -= qty;
        Touch();
        return Result.Success();
    }
}
