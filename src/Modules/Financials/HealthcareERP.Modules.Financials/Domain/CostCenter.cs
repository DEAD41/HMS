using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Financials.Domain;

public sealed class CostCenter : AggregateRoot
{
    private CostCenter() { }

    public Guid FacilityId { get; private set; }
    public string Code { get; private set; } = string.Empty;
    public string Name { get; private set; } = string.Empty;
    public string Status { get; private set; } = "Active";

    public static Result<CostCenter> Create(Guid facilityId, string code, string name)
    {
        if (facilityId == Guid.Empty) return Result.Failure<CostCenter>("Facility is required.");
        if (string.IsNullOrWhiteSpace(code)) return Result.Failure<CostCenter>("Cost center code is required.");
        if (string.IsNullOrWhiteSpace(name)) return Result.Failure<CostCenter>("Cost center name is required.");

        return Result.Success(new CostCenter
        {
            FacilityId = facilityId,
            Code = code.Trim().ToUpperInvariant(),
            Name = name.Trim(),
            Status = "Active"
        });
    }
}
