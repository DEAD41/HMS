using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class Charge : AggregateRoot
{
    private Charge() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid? EncounterId { get; private set; }
    public string ChargeCode { get; private set; } = string.Empty;
    public string Description { get; private set; } = string.Empty;
    public decimal Amount { get; private set; }
    public string Currency { get; private set; } = "USD";
    public Guid? SourceEventId { get; private set; }
    public string Status { get; private set; } = "Open";

    public static Result<Charge> Create(
        Guid facilityId,
        Guid patientId,
        string chargeCode,
        string description,
        decimal amount,
        string currency,
        Guid? encounterId,
        Guid? sourceEventId)
    {
        if (amount < 0) return Result.Failure<Charge>("Amount cannot be negative.");
        if (string.IsNullOrWhiteSpace(chargeCode)) return Result.Failure<Charge>("Charge code is required.");

        return Result.Success(new Charge
        {
            FacilityId = facilityId,
            PatientId = patientId,
            EncounterId = encounterId,
            ChargeCode = chargeCode.Trim().ToUpperInvariant(),
            Description = description.Trim(),
            Amount = amount,
            Currency = currency.Trim().ToUpperInvariant(),
            SourceEventId = sourceEventId,
            Status = "Open"
        });
    }
}
