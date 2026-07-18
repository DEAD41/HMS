using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class NursingCarePlan : AggregateRoot
{
    private NursingCarePlan() { }

    public Guid FacilityId { get; private set; }
    public Guid AdmissionId { get; private set; }
    public Guid PatientId { get; private set; }
    public string Summary { get; private set; } = string.Empty;
    public string Goals { get; private set; } = string.Empty;
    public string Status { get; private set; } = "Active";

    public static Result<NursingCarePlan> Create(
        Guid facilityId,
        Guid admissionId,
        Guid patientId,
        string summary,
        string goals)
    {
        if (admissionId == Guid.Empty || patientId == Guid.Empty)
            return Result.Failure<NursingCarePlan>("Admission and patient are required.");
        if (string.IsNullOrWhiteSpace(summary))
            return Result.Failure<NursingCarePlan>("Care plan summary is required.");

        return Result.Success(new NursingCarePlan
        {
            FacilityId = facilityId,
            AdmissionId = admissionId,
            PatientId = patientId,
            Summary = summary.Trim(),
            Goals = goals?.Trim() ?? string.Empty,
            Status = "Active"
        });
    }
}
