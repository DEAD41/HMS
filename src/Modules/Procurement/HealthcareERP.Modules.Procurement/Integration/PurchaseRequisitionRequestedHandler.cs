using System.Text.Json;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Infrastructure.Outbox;
using HealthcareERP.Modules.Procurement.Services;

namespace HealthcareERP.Modules.Procurement.Integration;

public sealed class PurchaseRequisitionRequestedHandler(ProcurementService procurementService) : IIntegrationEventHandler
{
    public string EventType => "PurchaseRequisitionRequested";

    public async Task HandleAsync(IntegrationEvent integrationEvent, CancellationToken cancellationToken = default)
    {
        using var doc = JsonDocument.Parse(integrationEvent.PayloadJson);
        var root = doc.RootElement;
        var signalId = root.GetProperty("SignalId").GetGuid();
        var itemId = root.GetProperty("ItemId").GetGuid();
        var storeId = root.GetProperty("StoreId").GetGuid();
        var qty = root.GetProperty("SuggestedQty").GetDecimal();
        var sku = root.TryGetProperty("Sku", out var skuEl) ? skuEl.GetString() : "ITEM";
        var name = root.TryGetProperty("Name", out var nameEl) ? nameEl.GetString() : "Item";

        var result = await procurementService.CreateRequisitionFromSignalAsync(
            integrationEvent.FacilityId,
            signalId,
            itemId,
            storeId,
            qty,
            $"Auto PR for {sku} - {name}",
            cancellationToken);

        if (result.IsFailure)
            throw new InvalidOperationException(result.Error);
    }
}
