using System.Text.Json;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Infrastructure.Outbox;
using HealthcareERP.Modules.Inventory.Services;

namespace HealthcareERP.Modules.Inventory.Integration;

public sealed class MedicationDispensedHandler(InventoryService inventoryService) : IIntegrationEventHandler
{
    public string EventType => "MedicationDispensed";

    public async Task HandleAsync(IntegrationEvent integrationEvent, CancellationToken cancellationToken = default)
    {
        using var doc = JsonDocument.Parse(integrationEvent.PayloadJson);
        var root = doc.RootElement;
        var itemId = root.GetProperty("ItemId").GetGuid();
        var storeId = root.GetProperty("StoreId").GetGuid();
        var quantity = root.GetProperty("Quantity").GetDecimal();

        // INV owns FEFO batch allocation; HMS never selects batch IDs.
        var result = await inventoryService.IssueAsync(
            integrationEvent.FacilityId,
            storeId,
            itemId,
            quantity,
            cancellationToken);

        if (result.IsFailure)
            throw new InvalidOperationException(result.Error);
    }
}
