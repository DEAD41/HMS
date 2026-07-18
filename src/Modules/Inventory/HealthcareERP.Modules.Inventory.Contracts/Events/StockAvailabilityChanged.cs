namespace HealthcareERP.Modules.Inventory.Contracts.Events;

public sealed record StockAvailabilityChanged(Guid ItemId, Guid StoreId, decimal QuantityOnHand, bool BelowReorder);
