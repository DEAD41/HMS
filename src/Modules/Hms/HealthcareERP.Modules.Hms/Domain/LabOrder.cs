using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class LabOrder : AggregateRoot
{
    private LabOrder() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid? EncounterId { get; private set; }
    public string TestCode { get; private set; } = string.Empty;
    public string TestName { get; private set; } = string.Empty;
    public string Status { get; private set; } = "Received";
    public string? SampleId { get; private set; }
    public string? ResultValue { get; private set; }
    public bool IsCritical { get; private set; }
    public string? AdapterSource { get; private set; }

    public static Result<LabOrder> Accept(Guid facilityId, Guid patientId, string testCode, string testName, Guid? encounterId)
    {
        if (string.IsNullOrWhiteSpace(testCode) || string.IsNullOrWhiteSpace(testName))
            return Result.Failure<LabOrder>("Test code and name are required.");
        return Result.Success(new LabOrder
        {
            FacilityId = facilityId,
            PatientId = patientId,
            EncounterId = encounterId,
            TestCode = testCode.Trim().ToUpperInvariant(),
            TestName = testName.Trim(),
            Status = "Received"
        });
    }

    public Result CollectSample(string? sampleId = null)
    {
        if (Status is "Final" or "Cancelled")
            return Result.Failure("Cannot collect sample for finalized/cancelled order.");
        SampleId = string.IsNullOrWhiteSpace(sampleId)
            ? $"SMP-{Guid.NewGuid():N}"[..16].ToUpperInvariant()
            : sampleId.Trim().ToUpperInvariant();
        Status = "Collected";
        Touch();
        return Result.Success();
    }

    public Result ImportFromAdapter(string resultValue, bool isCritical, string adapterSource)
    {
        if (Status is "Final")
            return Result.Failure("Order already finalized.");
        if (string.IsNullOrWhiteSpace(resultValue))
            return Result.Failure("Result value is required.");
        if (string.IsNullOrWhiteSpace(SampleId))
            SampleId = $"SMP-{Guid.NewGuid():N}"[..16].ToUpperInvariant();
        ResultValue = resultValue.Trim();
        IsCritical = isCritical;
        AdapterSource = adapterSource;
        Status = "Preliminary";
        Touch();
        return Result.Success();
    }

    public Result Finalize(string resultValue, bool isCritical)
    {
        if (string.IsNullOrWhiteSpace(resultValue)) return Result.Failure("Result value is required.");
        ResultValue = resultValue.Trim();
        IsCritical = isCritical;
        Status = "Final";
        Touch();
        return Result.Success();
    }
}
