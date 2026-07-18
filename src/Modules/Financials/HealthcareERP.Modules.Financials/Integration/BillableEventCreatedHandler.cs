using System.Text.Json;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Infrastructure.Outbox;
using HealthcareERP.Modules.Financials.Services;

namespace HealthcareERP.Modules.Financials.Integration;

public sealed class BillableEventCreatedHandler(ReceivableService receivableService) : IIntegrationEventHandler
{
    public string EventType => "BillableEventCreated";

    public async Task HandleAsync(IntegrationEvent integrationEvent, CancellationToken cancellationToken = default)
    {
        using var doc = JsonDocument.Parse(integrationEvent.PayloadJson);
        var root = doc.RootElement;
        var chargeId = root.GetProperty("Id").GetGuid();
        var patientId = root.GetProperty("PatientId").GetGuid();
        var chargeCode = root.GetProperty("ChargeCode").GetString() ?? "CHARGE";
        var amount = root.GetProperty("Amount").GetDecimal();
        var currency = root.GetProperty("Currency").GetString() ?? "USD";

        var result = await receivableService.CreateFromChargeAsync(
            integrationEvent.FacilityId,
            patientId,
            chargeId,
            chargeCode,
            amount,
            currency,
            cancellationToken);

        if (result.IsFailure)
            throw new InvalidOperationException(result.Error);
    }
}
