using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class Bed : AggregateRoot
{
    private Bed() { }

    public Guid FacilityId { get; private set; }
    public string Code { get; private set; } = string.Empty;
    public string Ward { get; private set; } = string.Empty;
    public string BedClass { get; private set; } = "General";
    public string Status { get; private set; } = "Available";

    public static Result<Bed> Create(Guid facilityId, string code, string ward, string bedClass)
    {
        if (facilityId == Guid.Empty) return Result.Failure<Bed>("Facility is required.");
        if (string.IsNullOrWhiteSpace(code)) return Result.Failure<Bed>("Bed code is required.");
        return Result.Success(new Bed
        {
            FacilityId = facilityId,
            Code = code.Trim().ToUpperInvariant(),
            Ward = ward.Trim(),
            BedClass = string.IsNullOrWhiteSpace(bedClass) ? "General" : bedClass.Trim(),
            Status = "Available"
        });
    }

    public Result Occupy()
    {
        if (Status != "Available") return Result.Failure("Bed is not available.");
        Status = "Occupied";
        Touch();
        return Result.Success();
    }

    public Result Release()
    {
        if (Status != "Occupied" && Status != "Blocked") return Result.Failure("Bed is not occupied.");
        Status = "Available";
        Touch();
        return Result.Success();
    }
}
