using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Foundation.Domain;

public sealed class OrgUnit : AggregateRoot
{
    private OrgUnit() { }

    public Guid FacilityId { get; private set; }
    public string Code { get; private set; } = string.Empty;
    public string Name { get; private set; } = string.Empty;
    public string Type { get; private set; } = "Department";
    public Guid? ParentId { get; private set; }
    public Guid? CostCenterRef { get; private set; }
    public string Status { get; private set; } = "Active";

    public static Result<OrgUnit> Create(Guid facilityId, string code, string name, string type, Guid? parentId = null, Guid? costCenterRef = null)
    {
        if (facilityId == Guid.Empty) return Result.Failure<OrgUnit>("Facility is required.");
        if (string.IsNullOrWhiteSpace(code)) return Result.Failure<OrgUnit>("Org unit code is required.");
        if (string.IsNullOrWhiteSpace(name)) return Result.Failure<OrgUnit>("Org unit name is required.");
        var allowed = new HashSet<string>(StringComparer.OrdinalIgnoreCase) { "Department", "Ward", "Clinic", "Store", "Theatre", "Other" };
        if (!allowed.Contains(type)) return Result.Failure<OrgUnit>("Invalid org unit type.");

        return Result.Success(new OrgUnit
        {
            FacilityId = facilityId,
            Code = code.Trim().ToUpperInvariant(),
            Name = name.Trim(),
            Type = type,
            ParentId = parentId,
            CostCenterRef = costCenterRef,
            Status = "Active"
        });
    }

    public Result Deactivate()
    {
        Status = "Inactive";
        Touch();
        return Result.Success();
    }
}
