using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class ErEncounter : AggregateRoot
{
    private ErEncounter() { }

    public Guid FacilityId { get; private set; }
    public Guid? PatientId { get; private set; }
    public string TemporaryId { get; private set; } = string.Empty;
    public string TriageCategory { get; private set; } = "Untriaged";
    public string Status { get; private set; } = "Arrived";
    public string? Disposition { get; private set; }

    public static Result<ErEncounter> Open(Guid facilityId, Guid? patientId, string? temporaryId)
    {
        if (facilityId == Guid.Empty) return Result.Failure<ErEncounter>("Facility is required.");

        return Result.Success(new ErEncounter
        {
            FacilityId = facilityId,
            PatientId = patientId,
            TemporaryId = string.IsNullOrWhiteSpace(temporaryId)
                ? $"UNK-{DateTimeOffset.UtcNow:yyyyMMddHHmmss}"
                : temporaryId.Trim().ToUpperInvariant(),
            Status = "Arrived",
            TriageCategory = "Untriaged"
        });
    }

    public Result Triage(string category)
    {
        if (string.IsNullOrWhiteSpace(category)) return Result.Failure("Triage category is required.");
        TriageCategory = category.Trim();
        Status = "Triaged";
        Touch();
        return Result.Success();
    }

    public Result Dispose(string disposition)
    {
        if (string.IsNullOrWhiteSpace(disposition)) return Result.Failure("Disposition is required.");
        Disposition = disposition.Trim();
        Status = "Disposed";
        Touch();
        return Result.Success();
    }
}
