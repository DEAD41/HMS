using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class Admission : AggregateRoot
{
    private Admission() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid AttendingClinicianId { get; private set; }
    public Guid? BedId { get; private set; }
    public string AdmittingDiagnosis { get; private set; } = string.Empty;
    public string Status { get; private set; } = "Admitted";

    public static Result<Admission> Admit(
        Guid facilityId,
        Guid patientId,
        Guid attendingClinicianId,
        Guid bedId,
        string admittingDiagnosis)
    {
        if (patientId == Guid.Empty || attendingClinicianId == Guid.Empty || bedId == Guid.Empty)
            return Result.Failure<Admission>("Patient, clinician, and bed are required.");
        if (string.IsNullOrWhiteSpace(admittingDiagnosis))
            return Result.Failure<Admission>("Admitting diagnosis is required.");

        return Result.Success(new Admission
        {
            FacilityId = facilityId,
            PatientId = patientId,
            AttendingClinicianId = attendingClinicianId,
            BedId = bedId,
            AdmittingDiagnosis = admittingDiagnosis.Trim(),
            Status = "Admitted"
        });
    }

    public Result InitiateDischarge()
    {
        if (Status != "Admitted" && Status != "Transferred")
            return Result.Failure("Admission is not active.");
        Status = "DischargeInitiated";
        Touch();
        return Result.Success();
    }

    public Result CompleteDischarge()
    {
        if (Status is not ("DischargeInitiated" or "Admitted"))
            return Result.Failure("Discharge cannot be completed from current status.");
        Status = "Discharged";
        Touch();
        return Result.Success();
    }
}
