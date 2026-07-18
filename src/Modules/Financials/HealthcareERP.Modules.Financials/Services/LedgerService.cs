using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Financials.Domain;
using HealthcareERP.Modules.Financials.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Financials.Services;

public sealed class LedgerService(FinancialsDbContext db, IAuditWriter auditWriter)
{
    public async Task<Result<Account>> CreateAccountAsync(Guid facilityId, string code, string name, string type, CancellationToken cancellationToken = default)
    {
        if (await db.Accounts.AnyAsync(x => x.FacilityId == facilityId && x.Code == code.Trim().ToUpperInvariant(), cancellationToken))
            return Result.Failure<Account>("Account code already exists.");

        var create = Account.Create(facilityId, code, name, type);
        if (create.IsFailure) return create;
        db.Accounts.Add(create.Value!);
        await auditWriter.WriteAsync("FIN", "Create", nameof(Account), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public Task<List<Account>> ListAccountsAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.Accounts.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderBy(x => x.Code).ToListAsync(cancellationToken);

    public Task<List<PayrollExpense>> ListPayrollExpensesAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.PayrollExpenses.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderByDescending(x => x.CreatedAt).ToListAsync(cancellationToken);

    public async Task<Result<CostCenter>> CreateCostCenterAsync(Guid facilityId, string code, string name, CancellationToken cancellationToken = default)
    {
        if (await db.CostCenters.AnyAsync(x => x.FacilityId == facilityId && x.Code == code.Trim().ToUpperInvariant(), cancellationToken))
            return Result.Failure<CostCenter>("Cost center code already exists.");

        var create = CostCenter.Create(facilityId, code, name);
        if (create.IsFailure) return create;
        db.CostCenters.Add(create.Value!);
        await auditWriter.WriteAsync("FIN", "Create", nameof(CostCenter), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }
}
