using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class DischargeProcess : AggregateRoot
{
    private DischargeProcess() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid AdmissionId { get; private set; }
    public string Summary { get; private set; } = string.Empty;
    public string Status { get; private set; } = "Initiated";
    public Guid? FollowUpAppointmentId { get; private set; }

    public static Result<DischargeProcess> Initiate(Guid facilityId, Guid patientId, Guid admissionId)
    {
        if (admissionId == Guid.Empty) return Result.Failure<DischargeProcess>("Admission is required.");
        return Result.Success(new DischargeProcess
        {
            FacilityId = facilityId,
            PatientId = patientId,
            AdmissionId = admissionId,
            Status = "Initiated"
        });
    }

    public Result Complete(string summary, Guid? followUpAppointmentId)
    {
        if (string.IsNullOrWhiteSpace(summary)) return Result.Failure("Discharge summary is required.");
        Summary = summary.Trim();
        FollowUpAppointmentId = followUpAppointmentId;
        Status = "Completed";
        Touch();
        return Result.Success();
    }
}
