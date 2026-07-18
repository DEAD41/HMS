using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Financials.Domain;

public sealed class PayrollExpense : AggregateRoot
{
    private PayrollExpense() { }

    public Guid FacilityId { get; private set; }
    public Guid PayrollRunId { get; private set; }
    public string Period { get; private set; } = string.Empty;
    public decimal GrossAmount { get; private set; }
    public decimal NetAmount { get; private set; }
    public string Status { get; private set; } = "Posted";

    public static Result<PayrollExpense> FromPayroll(Guid facilityId, Guid payrollRunId, string period, decimal gross, decimal net)
    {
        if (payrollRunId == Guid.Empty) return Result.Failure<PayrollExpense>("Payroll run is required.");
        return Result.Success(new PayrollExpense
        {
            FacilityId = facilityId,
            PayrollRunId = payrollRunId,
            Period = period,
            GrossAmount = gross,
            NetAmount = net,
            Status = "Posted"
        });
    }
}
