using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Financials.Domain;

public sealed class BudgetLine : AggregateRoot
{
    private BudgetLine() { }

    public Guid FacilityId { get; private set; }
    public Guid CostCenterId { get; private set; }
    public string Period { get; private set; } = string.Empty;
    public string AccountCode { get; private set; } = string.Empty;
    public decimal Amount { get; private set; }
    public decimal ActualAmount { get; private set; }
    public string Status { get; private set; } = "Draft";

    public decimal Variance => Amount - ActualAmount;
    public decimal UtilizationPercent => Amount == 0 ? 0 : Math.Round(ActualAmount / Amount * 100m, 2);

    public static Result<BudgetLine> Create(Guid facilityId, Guid costCenterId, string period, string accountCode, decimal amount)
    {
        if (facilityId == Guid.Empty || costCenterId == Guid.Empty)
            return Result.Failure<BudgetLine>("Facility and cost center are required.");
        if (string.IsNullOrWhiteSpace(period)) return Result.Failure<BudgetLine>("Period is required.");
        if (amount < 0) return Result.Failure<BudgetLine>("Budget amount cannot be negative.");

        return Result.Success(new BudgetLine
        {
            FacilityId = facilityId,
            CostCenterId = costCenterId,
            Period = period.Trim(),
            AccountCode = string.IsNullOrWhiteSpace(accountCode) ? "OPEX" : accountCode.Trim().ToUpperInvariant(),
            Amount = amount,
            ActualAmount = 0,
            Status = "Draft"
        });
    }

    public Result Activate()
    {
        if (Status is "Closed") return Result.Failure("Closed budgets cannot be activated.");
        Status = "Active";
        Touch();
        return Result.Success();
    }

    public Result RecordActual(decimal amount)
    {
        if (Status != "Active") return Result.Failure("Only active budgets accept actuals.");
        if (amount < 0) return Result.Failure("Actual amount cannot be negative.");
        ActualAmount += amount;
        Touch();
        return Result.Success();
    }

    public bool IsOverBudget(decimal thresholdPercent = 100m) => UtilizationPercent >= thresholdPercent;
}
