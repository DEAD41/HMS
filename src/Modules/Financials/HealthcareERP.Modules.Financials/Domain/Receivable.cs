using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Financials.Domain;

public sealed class Receivable : AggregateRoot
{
    private Receivable() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid SourceChargeId { get; private set; }
    public string ChargeCode { get; private set; } = string.Empty;
    public decimal Amount { get; private set; }
    public string Currency { get; private set; } = "USD";
    public string Status { get; private set; } = "Open";
    public decimal SettledAmount { get; private set; }

    public static Result<Receivable> FromCharge(
        Guid facilityId,
        Guid patientId,
        Guid sourceChargeId,
        string chargeCode,
        decimal amount,
        string currency)
    {
        if (amount < 0) return Result.Failure<Receivable>("Amount cannot be negative.");
        return Result.Success(new Receivable
        {
            FacilityId = facilityId,
            PatientId = patientId,
            SourceChargeId = sourceChargeId,
            ChargeCode = chargeCode.Trim().ToUpperInvariant(),
            Amount = amount,
            Currency = currency.Trim().ToUpperInvariant(),
            Status = "Open"
        });
    }

    public Result ApplyPayment(decimal amount)
    {
        if (amount <= 0) return Result.Failure("Payment must be positive.");
        SettledAmount += amount;
        Status = SettledAmount >= Amount ? "Settled" : "PartiallySettled";
        Touch();
        return Result.Success();
    }
}
