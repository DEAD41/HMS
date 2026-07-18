using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Financials.Domain;
using HealthcareERP.Modules.Financials.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Financials.Services;

public sealed class BudgetService(FinancialsDbContext db, IAuditWriter auditWriter)
{
    public async Task<Result<BudgetLine>> CreateAsync(
        Guid facilityId,
        Guid costCenterId,
        string period,
        string accountCode,
        decimal amount,
        CancellationToken cancellationToken = default)
    {
        if (!await db.CostCenters.AnyAsync(x => x.Id == costCenterId && x.FacilityId == facilityId, cancellationToken))
            return Result.Failure<BudgetLine>("Cost center not found.");

        var create = BudgetLine.Create(facilityId, costCenterId, period, accountCode, amount);
        if (create.IsFailure) return create;
        db.BudgetLines.Add(create.Value!);
        await auditWriter.WriteAsync("FIN", "CreateBudget", nameof(BudgetLine), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<BudgetLine>> ActivateAsync(Guid budgetId, CancellationToken cancellationToken = default)
    {
        var line = await db.BudgetLines.FirstOrDefaultAsync(x => x.Id == budgetId, cancellationToken);
        if (line is null) return Result.Failure<BudgetLine>("Budget line not found.");
        var activate = line.Activate();
        if (activate.IsFailure) return Result.Failure<BudgetLine>(activate.Error!);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(line);
    }

    public async Task<Result<BudgetLine>> RecordActualAsync(Guid budgetId, decimal amount, CancellationToken cancellationToken = default)
    {
        var line = await db.BudgetLines.FirstOrDefaultAsync(x => x.Id == budgetId, cancellationToken);
        if (line is null) return Result.Failure<BudgetLine>("Budget line not found.");
        var record = line.RecordActual(amount);
        if (record.IsFailure) return Result.Failure<BudgetLine>(record.Error!);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(line);
    }

    public Task<List<BudgetLine>> ListAsync(Guid facilityId, string? period, CancellationToken cancellationToken = default)
    {
        var q = db.BudgetLines.AsNoTracking().Where(x => x.FacilityId == facilityId);
        if (!string.IsNullOrWhiteSpace(period)) q = q.Where(x => x.Period == period.Trim());
        return q.OrderByDescending(x => x.CreatedAt).ToListAsync(cancellationToken);
    }

    public async Task<List<object>> VarianceAsync(Guid facilityId, string? period, CancellationToken cancellationToken = default)
    {
        var lines = await ListAsync(facilityId, period, cancellationToken);
        return lines.Select(x => (object)new
        {
            x.Id,
            x.CostCenterId,
            x.Period,
            x.AccountCode,
            x.Amount,
            x.ActualAmount,
            x.Variance,
            x.UtilizationPercent,
            OverBudget = x.IsOverBudget(),
            x.Status
        }).ToList();
    }
}
