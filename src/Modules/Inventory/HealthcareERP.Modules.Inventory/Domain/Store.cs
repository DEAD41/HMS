using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Inventory.Domain;

public sealed class Store : AggregateRoot
{
    private Store() { }

    public Guid FacilityId { get; private set; }
    public string Code { get; private set; } = string.Empty;
    public string Name { get; private set; } = string.Empty;
    public string Status { get; private set; } = "Active";

    public static Result<Store> Create(Guid facilityId, string code, string name)
    {
        if (string.IsNullOrWhiteSpace(code)) return Result.Failure<Store>("Store code is required.");
        if (string.IsNullOrWhiteSpace(name)) return Result.Failure<Store>("Store name is required.");
        return Result.Success(new Store
        {
            FacilityId = facilityId,
            Code = code.Trim().ToUpperInvariant(),
            Name = name.Trim(),
            Status = "Active"
        });
    }
}
