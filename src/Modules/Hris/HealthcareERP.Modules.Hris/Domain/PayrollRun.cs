using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hris.Domain;

public sealed class PayrollRun : AggregateRoot
{
    private PayrollRun() { }

    public Guid FacilityId { get; private set; }
    public string Period { get; private set; } = string.Empty;
    public decimal GrossAmount { get; private set; }
    public decimal Deductions { get; private set; }
    public decimal NetAmount { get; private set; }
    public string Status { get; private set; } = "Open";

    public static Result<PayrollRun> Create(Guid facilityId, string period, decimal grossAmount, decimal deductions)
    {
        if (string.IsNullOrWhiteSpace(period)) return Result.Failure<PayrollRun>("Period is required.");
        if (grossAmount < 0 || deductions < 0) return Result.Failure<PayrollRun>("Amounts cannot be negative.");
        if (deductions > grossAmount) return Result.Failure<PayrollRun>("Deductions cannot exceed gross.");

        return Result.Success(new PayrollRun
        {
            FacilityId = facilityId,
            Period = period.Trim(),
            GrossAmount = grossAmount,
            Deductions = deductions,
            NetAmount = grossAmount - deductions,
            Status = "Calculated"
        });
    }

    public Result Post()
    {
        if (Status is not ("Calculated" or "Approved"))
            return Result.Failure("Payroll must be calculated/approved before posting.");
        Status = "Posted";
        Touch();
        return Result.Success();
    }
}
