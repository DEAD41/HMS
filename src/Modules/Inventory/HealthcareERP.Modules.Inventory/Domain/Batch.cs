using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Inventory.Domain;

public sealed class Batch : AggregateRoot
{
    private Batch() { }

    public Guid FacilityId { get; private set; }
    public Guid StoreId { get; private set; }
    public Guid ItemId { get; private set; }
    public string BatchNumber { get; private set; } = string.Empty;
    public DateOnly ExpiryDate { get; private set; }
    public decimal QuantityOnHand { get; private set; }
    public string Status { get; private set; } = "Available";

    public bool IsAvailable(DateOnly asOf) =>
        Status == "Available" && ExpiryDate >= asOf && QuantityOnHand > 0;

    public static Result<Batch> Receive(
        Guid facilityId,
        Guid storeId,
        Guid itemId,
        string batchNumber,
        DateOnly expiryDate,
        decimal quantity)
    {
        if (facilityId == Guid.Empty || storeId == Guid.Empty || itemId == Guid.Empty)
            return Result.Failure<Batch>("Facility, store, and item are required.");
        if (string.IsNullOrWhiteSpace(batchNumber))
            return Result.Failure<Batch>("Batch number is required.");
        if (quantity <= 0)
            return Result.Failure<Batch>("Quantity must be positive.");
        if (expiryDate < DateOnly.FromDateTime(DateTime.UtcNow))
            return Result.Failure<Batch>("Cannot receive an expired batch.");

        return Result.Success(new Batch
        {
            FacilityId = facilityId,
            StoreId = storeId,
            ItemId = itemId,
            BatchNumber = batchNumber.Trim().ToUpperInvariant(),
            ExpiryDate = expiryDate,
            QuantityOnHand = quantity,
            Status = "Available"
        });
    }

    public Result Increase(decimal quantity)
    {
        if (quantity <= 0) return Result.Failure("Quantity must be positive.");
        if (Status == "Expired" || Status == "Hold")
            return Result.Failure($"Cannot increase a {Status.ToLowerInvariant()} batch.");
        QuantityOnHand += quantity;
        Touch();
        return Result.Success();
    }

    public Result Decrease(decimal quantity)
    {
        if (quantity <= 0) return Result.Failure("Quantity must be positive.");
        if (Status == "Hold") return Result.Failure("Batch is on hold.");
        if (ExpiryDate < DateOnly.FromDateTime(DateTime.UtcNow))
        {
            Status = "Expired";
            return Result.Failure("Expired batches cannot be issued.");
        }
        if (quantity > QuantityOnHand) return Result.Failure("Insufficient batch quantity.");
        QuantityOnHand -= quantity;
        if (QuantityOnHand == 0) Status = "Depleted";
        Touch();
        return Result.Success();
    }

    public Result PlaceHold()
    {
        if (Status != "Available") return Result.Failure("Only available batches can be held.");
        Status = "Hold";
        Touch();
        return Result.Success();
    }
}

public sealed record BatchAllocation(Guid BatchId, string BatchNumber, DateOnly ExpiryDate, decimal Quantity);
