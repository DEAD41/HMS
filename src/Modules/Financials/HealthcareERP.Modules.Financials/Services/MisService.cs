using HealthcareERP.Modules.Financials.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Financials.Services;

public sealed class MisService(FinancialsDbContext db)
{
    public async Task<object> GetDashboardAsync(Guid facilityId, CancellationToken cancellationToken = default)
    {
        var receivables = await db.Receivables.AsNoTracking().Where(x => x.FacilityId == facilityId).ToListAsync(cancellationToken);
        var invoices = await db.VendorInvoices.AsNoTracking().Where(x => x.FacilityId == facilityId).ToListAsync(cancellationToken);
        var payroll = await db.PayrollExpenses.AsNoTracking().Where(x => x.FacilityId == facilityId).ToListAsync(cancellationToken);
        var budgets = await db.BudgetLines.AsNoTracking().Where(x => x.FacilityId == facilityId && x.Status == "Active").ToListAsync(cancellationToken);

        var arOpen = receivables.Where(x => x.Status != "Settled").Sum(x => x.Amount - x.SettledAmount);
        var arTotal = receivables.Sum(x => x.Amount);
        var apOpen = invoices.Where(x => x.Status != "Paid").Sum(x => x.Amount);
        var payrollNet = payroll.Sum(x => x.NetAmount);
        var budgetTotal = budgets.Sum(x => x.Amount);
        var budgetActual = budgets.Sum(x => x.ActualAmount);
        var patientCount = receivables.Select(x => x.PatientId).Where(x => x != Guid.Empty).Distinct().Count();
        var costPerPatient = patientCount == 0 ? 0 : Math.Round((budgetActual + payrollNet) / patientCount, 2);

        return new
        {
            FacilityId = facilityId,
            GeneratedAt = DateTimeOffset.UtcNow,
            Kpis = new
            {
                ArOpen = arOpen,
                ArTotal = arTotal,
                ApOpen = apOpen,
                PayrollExpenseNet = payrollNet,
                BudgetTotal = budgetTotal,
                BudgetActual = budgetActual,
                BudgetUtilizationPercent = budgetTotal == 0 ? 0 : Math.Round(budgetActual / budgetTotal * 100m, 2),
                CostPerPatient = costPerPatient,
                ActiveBudgets = budgets.Count,
                OverBudgetLines = budgets.Count(x => x.IsOverBudget())
            },
            Pnl = new
            {
                Revenue = arTotal,
                OperatingExpense = budgetActual + payrollNet + invoices.Sum(x => x.Amount),
                Net = arTotal - (budgetActual + payrollNet + invoices.Sum(x => x.Amount))
            }
        };
    }
}
