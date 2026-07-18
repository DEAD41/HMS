using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Procurement.Domain;

public sealed class Vendor : AggregateRoot
{
    private Vendor() { }

    public Guid FacilityId { get; private set; }
    public string Code { get; private set; } = string.Empty;
    public string Name { get; private set; } = string.Empty;
    public string Status { get; private set; } = "Active";

    public static Result<Vendor> Create(Guid facilityId, string code, string name)
    {
        if (string.IsNullOrWhiteSpace(code)) return Result.Failure<Vendor>("Vendor code is required.");
        if (string.IsNullOrWhiteSpace(name)) return Result.Failure<Vendor>("Vendor name is required.");
        return Result.Success(new Vendor
        {
            FacilityId = facilityId,
            Code = code.Trim().ToUpperInvariant(),
            Name = name.Trim(),
            Status = "Active"
        });
    }
}
