using System.Text.Json;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Infrastructure.Outbox;
using HealthcareERP.Modules.Financials.Domain;
using HealthcareERP.Modules.Financials.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Financials.Integration;

public sealed class PayrollPostedHandler(FinancialsDbContext db) : IIntegrationEventHandler
{
    public string EventType => "PayrollPosted";

    public async Task HandleAsync(IntegrationEvent integrationEvent, CancellationToken cancellationToken = default)
    {
        using var doc = JsonDocument.Parse(integrationEvent.PayloadJson);
        var root = doc.RootElement;
        var payrollRunId = root.GetProperty("PayrollRunId").GetGuid();
        if (await db.PayrollExpenses.AnyAsync(x => x.PayrollRunId == payrollRunId, cancellationToken))
            return;

        var period = root.GetProperty("Period").GetString() ?? string.Empty;
        var gross = root.GetProperty("GrossAmount").GetDecimal();
        var net = root.GetProperty("NetAmount").GetDecimal();
        var create = PayrollExpense.FromPayroll(integrationEvent.FacilityId, payrollRunId, period, gross, net);
        if (create.IsFailure) throw new InvalidOperationException(create.Error);

        db.PayrollExpenses.Add(create.Value!);
        await db.SaveChangesAsync(cancellationToken);
    }
}
