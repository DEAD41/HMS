using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class Appointment : AggregateRoot
{
    private Appointment() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid ClinicianEmployeeId { get; private set; }
    public Guid? ClinicOrgUnitId { get; private set; }
    public DateTimeOffset StartsAt { get; private set; }
    public DateTimeOffset EndsAt { get; private set; }
    public string Status { get; private set; } = "Scheduled";
    public string? Reason { get; private set; }

    public static Result<Appointment> Schedule(
        Guid facilityId,
        Guid patientId,
        Guid clinicianEmployeeId,
        DateTimeOffset startsAt,
        DateTimeOffset endsAt,
        Guid? clinicOrgUnitId,
        string? reason)
    {
        if (endsAt <= startsAt) return Result.Failure<Appointment>("Appointment end must be after start.");
        if (patientId == Guid.Empty || clinicianEmployeeId == Guid.Empty)
            return Result.Failure<Appointment>("Patient and clinician are required.");

        return Result.Success(new Appointment
        {
            FacilityId = facilityId,
            PatientId = patientId,
            ClinicianEmployeeId = clinicianEmployeeId,
            ClinicOrgUnitId = clinicOrgUnitId,
            StartsAt = startsAt,
            EndsAt = endsAt,
            Reason = reason,
            Status = "Scheduled"
        });
    }

    public Result CheckIn()
    {
        if (Status is not ("Scheduled")) return Result.Failure("Only scheduled appointments can be checked in.");
        Status = "CheckedIn";
        Touch();
        return Result.Success();
    }
}
