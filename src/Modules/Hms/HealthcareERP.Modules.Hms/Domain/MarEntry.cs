using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class MarEntry : AggregateRoot
{
    private MarEntry() { }

    public Guid FacilityId { get; private set; }
    public Guid AdmissionId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid MedicationDispenseId { get; private set; }
    public Guid NurseEmployeeId { get; private set; }
    public string DoseInstanceId { get; private set; } = string.Empty;
    public string MedicationName { get; private set; } = string.Empty;
    public string Status { get; private set; } = "Due";
    public string? Notes { get; private set; }
    public DateTimeOffset? AdministeredAt { get; private set; }

    public static Result<MarEntry> Schedule(
        Guid facilityId,
        Guid admissionId,
        Guid patientId,
        Guid medicationDispenseId,
        Guid nurseEmployeeId,
        string doseInstanceId,
        string medicationName)
    {
        if (admissionId == Guid.Empty || medicationDispenseId == Guid.Empty || nurseEmployeeId == Guid.Empty)
            return Result.Failure<MarEntry>("Admission, dispense, and nurse are required.");
        if (string.IsNullOrWhiteSpace(doseInstanceId))
            return Result.Failure<MarEntry>("Dose instance id is required.");

        return Result.Success(new MarEntry
        {
            FacilityId = facilityId,
            AdmissionId = admissionId,
            PatientId = patientId,
            MedicationDispenseId = medicationDispenseId,
            NurseEmployeeId = nurseEmployeeId,
            DoseInstanceId = doseInstanceId.Trim(),
            MedicationName = medicationName.Trim(),
            Status = "Due"
        });
    }

    public Result Administer(string? notes)
    {
        if (Status == "Administered")
            return Result.Failure("MAR dose already administered and cannot be changed.");
        if (Status is not ("Due" or "Held"))
            return Result.Failure($"Cannot administer from status {Status}.");
        Status = "Administered";
        Notes = notes?.Trim();
        AdministeredAt = DateTimeOffset.UtcNow;
        Touch();
        return Result.Success();
    }

    public Result Hold(string? notes)
    {
        if (Status == "Administered")
            return Result.Failure("Administered MAR cannot be held.");
        if (Status != "Due") return Result.Failure("Only due doses can be held.");
        Status = "Held";
        Notes = notes?.Trim();
        Touch();
        return Result.Success();
    }

    public Result Refuse(string? notes)
    {
        if (Status == "Administered")
            return Result.Failure("Administered MAR cannot be refused.");
        if (Status != "Due") return Result.Failure("Only due doses can be refused.");
        Status = "Refused";
        Notes = notes?.Trim();
        Touch();
        return Result.Success();
    }

    public Result Miss(string? notes)
    {
        if (Status == "Administered")
            return Result.Failure("Administered MAR cannot be marked missed.");
        if (Status != "Due") return Result.Failure("Only due doses can be missed.");
        Status = "Missed";
        Notes = notes?.Trim();
        Touch();
        return Result.Success();
    }
}
