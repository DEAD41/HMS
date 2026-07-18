using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Inventory.Domain;

public sealed class Item : AggregateRoot
{
    private Item() { }

    public Guid FacilityId { get; private set; }
    public string Sku { get; private set; } = string.Empty;
    public string Name { get; private set; } = string.Empty;
    public string UnitOfMeasure { get; private set; } = "EA";
    public bool BatchControlled { get; private set; }
    public decimal ReorderLevel { get; private set; }
    public string Status { get; private set; } = "Active";

    public static Result<Item> Create(Guid facilityId, string sku, string name, string uom, bool batchControlled, decimal reorderLevel)
    {
        if (string.IsNullOrWhiteSpace(sku)) return Result.Failure<Item>("SKU is required.");
        if (string.IsNullOrWhiteSpace(name)) return Result.Failure<Item>("Name is required.");
        if (reorderLevel < 0) return Result.Failure<Item>("Reorder level cannot be negative.");

        return Result.Success(new Item
        {
            FacilityId = facilityId,
            Sku = sku.Trim().ToUpperInvariant(),
            Name = name.Trim(),
            UnitOfMeasure = uom.Trim().ToUpperInvariant(),
            BatchControlled = batchControlled,
            ReorderLevel = reorderLevel,
            Status = "Active"
        });
    }
}
