using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class RadiologyOrder : AggregateRoot
{
    private RadiologyOrder() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid? EncounterId { get; private set; }
    public string Modality { get; private set; } = string.Empty;
    public string StudyName { get; private set; } = string.Empty;
    public string Status { get; private set; } = "Ordered";
    public string? ReportText { get; private set; }
    public string? AccessionNumber { get; private set; }
    public string? StudyInstanceUid { get; private set; }
    public string? AdapterSource { get; private set; }

    public static Result<RadiologyOrder> Accept(
        Guid facilityId,
        Guid patientId,
        string modality,
        string studyName,
        Guid? encounterId)
    {
        if (string.IsNullOrWhiteSpace(modality) || string.IsNullOrWhiteSpace(studyName))
            return Result.Failure<RadiologyOrder>("Modality and study name are required.");
        return Result.Success(new RadiologyOrder
        {
            FacilityId = facilityId,
            PatientId = patientId,
            EncounterId = encounterId,
            Modality = modality.Trim().ToUpperInvariant(),
            StudyName = studyName.Trim(),
            Status = "Ordered",
            AccessionNumber = $"ACC-{Guid.NewGuid():N}"[..16].ToUpperInvariant()
        });
    }

    public Result AcquireFromAdapter(string studyInstanceUid, string adapterSource)
    {
        if (Status is "Reported" or "Cancelled")
            return Result.Failure("Cannot acquire study for reported/cancelled order.");
        if (string.IsNullOrWhiteSpace(studyInstanceUid))
            return Result.Failure("StudyInstanceUid is required.");
        StudyInstanceUid = studyInstanceUid.Trim();
        AdapterSource = adapterSource;
        Status = "Acquired";
        Touch();
        return Result.Success();
    }

    public Result SignReport(string reportText)
    {
        if (string.IsNullOrWhiteSpace(reportText)) return Result.Failure("Report text is required.");
        if (Status is not ("Ordered" or "Acquired" or "Reporting"))
            return Result.Failure("Study must be ordered/acquired before signing.");
        ReportText = reportText.Trim();
        Status = "Reported";
        Touch();
        return Result.Success();
    }
}
