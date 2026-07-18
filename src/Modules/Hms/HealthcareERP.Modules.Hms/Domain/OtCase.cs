using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class OtCase : AggregateRoot
{
    private OtCase() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid SurgeonEmployeeId { get; private set; }
    public string TheatreCode { get; private set; } = string.Empty;
    public string ProcedureName { get; private set; } = string.Empty;
    public DateTimeOffset ScheduledAt { get; private set; }
    public bool ChecklistComplete { get; private set; }
    public string Status { get; private set; } = "Scheduled";

    public static Result<OtCase> Schedule(
        Guid facilityId,
        Guid patientId,
        Guid surgeonEmployeeId,
        string theatreCode,
        string procedureName,
        DateTimeOffset scheduledAt)
    {
        if (patientId == Guid.Empty || surgeonEmployeeId == Guid.Empty)
            return Result.Failure<OtCase>("Patient and surgeon are required.");
        if (string.IsNullOrWhiteSpace(theatreCode) || string.IsNullOrWhiteSpace(procedureName))
            return Result.Failure<OtCase>("Theatre and procedure are required.");

        return Result.Success(new OtCase
        {
            FacilityId = facilityId,
            PatientId = patientId,
            SurgeonEmployeeId = surgeonEmployeeId,
            TheatreCode = theatreCode.Trim().ToUpperInvariant(),
            ProcedureName = procedureName.Trim(),
            ScheduledAt = scheduledAt,
            Status = "Scheduled"
        });
    }

    public Result CompleteChecklist()
    {
        ChecklistComplete = true;
        Status = "PreOp";
        Touch();
        return Result.Success();
    }

    public Result Complete()
    {
        if (!ChecklistComplete) return Result.Failure("Pre-op checklist must be complete.");
        Status = "Completed";
        Touch();
        return Result.Success();
    }
}
