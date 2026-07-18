using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class OpdEncounter : AggregateRoot
{
    private OpdEncounter() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid? AppointmentId { get; private set; }
    public Guid ClinicianEmployeeId { get; private set; }
    public string Status { get; private set; } = "Open";
    public string? ChiefComplaint { get; private set; }
    public string? Disposition { get; private set; }

    public static Result<OpdEncounter> Open(Guid facilityId, Guid patientId, Guid clinicianEmployeeId, Guid? appointmentId, string? chiefComplaint)
    {
        return Result.Success(new OpdEncounter
        {
            FacilityId = facilityId,
            PatientId = patientId,
            ClinicianEmployeeId = clinicianEmployeeId,
            AppointmentId = appointmentId,
            ChiefComplaint = chiefComplaint,
            Status = "Open"
        });
    }

    public Result Close(string disposition)
    {
        if (Status == "Closed") return Result.Failure("Encounter already closed.");
        if (string.IsNullOrWhiteSpace(disposition)) return Result.Failure("Disposition is required.");
        Status = "Closed";
        Disposition = disposition.Trim();
        Touch();
        return Result.Success();
    }
}
