using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Inventory.Contracts.Events;
using HealthcareERP.Modules.Inventory.Domain;
using HealthcareERP.Modules.Inventory.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Inventory.Services;

public sealed class InventoryService(
    InventoryDbContext db,
    IIntegrationEventPublisher publisher,
    IAuditWriter auditWriter)
{
    public async Task<Result<Item>> CreateItemAsync(Guid facilityId, string sku, string name, string uom, bool batchControlled, decimal reorderLevel, CancellationToken cancellationToken = default)
    {
        if (await db.Items.AnyAsync(x => x.FacilityId == facilityId && x.Sku == sku.Trim().ToUpperInvariant(), cancellationToken))
            return Result.Failure<Item>("SKU already exists.");

        var create = Item.Create(facilityId, sku, name, uom, batchControlled, reorderLevel);
        if (create.IsFailure) return create;
        db.Items.Add(create.Value!);
        await auditWriter.WriteAsync("INV", "Create", nameof(Item), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<Store>> CreateStoreAsync(Guid facilityId, string code, string name, CancellationToken cancellationToken = default)
    {
        if (await db.Stores.AnyAsync(x => x.FacilityId == facilityId && x.Code == code.Trim().ToUpperInvariant(), cancellationToken))
            return Result.Failure<Store>("Store code already exists.");

        var create = Store.Create(facilityId, code, name);
        if (create.IsFailure) return create;
        db.Stores.Add(create.Value!);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<(StockBalance Balance, Batch? Batch)>> ReceiveAsync(
        Guid facilityId,
        Guid storeId,
        Guid itemId,
        decimal quantity,
        string? batchNumber = null,
        DateOnly? expiryDate = null,
        CancellationToken cancellationToken = default)
    {
        var item = await db.Items.FirstOrDefaultAsync(x => x.Id == itemId && x.FacilityId == facilityId, cancellationToken);
        if (item is null) return Result.Failure<(StockBalance, Batch?)>("Item not found.");
        if (!await db.Stores.AnyAsync(x => x.Id == storeId && x.FacilityId == facilityId, cancellationToken))
            return Result.Failure<(StockBalance, Batch?)>("Store not found.");

        Batch? batch = null;
        if (item.BatchControlled)
        {
            if (string.IsNullOrWhiteSpace(batchNumber) || expiryDate is null)
                return Result.Failure<(StockBalance, Batch?)>("Batch number and expiry are required for batch-controlled items.");

            var normalized = batchNumber.Trim().ToUpperInvariant();
            batch = await db.Batches.FirstOrDefaultAsync(x =>
                x.FacilityId == facilityId &&
                x.StoreId == storeId &&
                x.ItemId == itemId &&
                x.BatchNumber == normalized, cancellationToken);

            if (batch is null)
            {
                var createBatch = Batch.Receive(facilityId, storeId, itemId, normalized, expiryDate.Value, quantity);
                if (createBatch.IsFailure) return Result.Failure<(StockBalance, Batch?)>(createBatch.Error!);
                batch = createBatch.Value!;
                db.Batches.Add(batch);
            }
            else
            {
                if (batch.ExpiryDate != expiryDate.Value)
                    return Result.Failure<(StockBalance, Batch?)>("Existing batch expiry does not match.");
                var increaseBatch = batch.Increase(quantity);
                if (increaseBatch.IsFailure) return Result.Failure<(StockBalance, Batch?)>(increaseBatch.Error!);
            }
        }

        var balance = await db.StockBalances.FirstOrDefaultAsync(x => x.StoreId == storeId && x.ItemId == itemId, cancellationToken);
        if (balance is null)
        {
            balance = StockBalance.Create(facilityId, storeId, itemId);
            db.StockBalances.Add(balance);
        }

        var increase = balance.Increase(quantity);
        if (increase.IsFailure) return Result.Failure<(StockBalance, Batch?)>(increase.Error!);

        await PublishAvailabilityAsync(item, balance, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success((balance, batch));
    }

    public async Task<Result<(StockBalance Balance, IReadOnlyList<BatchAllocation> Allocations)>> IssueAsync(
        Guid facilityId,
        Guid storeId,
        Guid itemId,
        decimal quantity,
        CancellationToken cancellationToken = default)
    {
        var item = await db.Items.FirstOrDefaultAsync(x => x.Id == itemId && x.FacilityId == facilityId, cancellationToken);
        if (item is null) return Result.Failure<(StockBalance, IReadOnlyList<BatchAllocation>)>("Item not found.");

        var balance = await db.StockBalances.FirstOrDefaultAsync(x => x.StoreId == storeId && x.ItemId == itemId, cancellationToken);
        if (balance is null) return Result.Failure<(StockBalance, IReadOnlyList<BatchAllocation>)>("No stock balance.");

        var allocations = new List<BatchAllocation>();
        if (item.BatchControlled)
        {
            var today = DateOnly.FromDateTime(DateTime.UtcNow);
            var batches = await db.Batches
                .Where(x => x.FacilityId == facilityId && x.StoreId == storeId && x.ItemId == itemId && x.Status == "Available")
                .OrderBy(x => x.ExpiryDate)
                .ThenBy(x => x.BatchNumber)
                .ToListAsync(cancellationToken);

            var remaining = quantity;
            foreach (var batch in batches)
            {
                if (!batch.IsAvailable(today) || remaining <= 0) continue;
                var take = Math.Min(batch.QuantityOnHand, remaining);
                var decreaseBatch = batch.Decrease(take);
                if (decreaseBatch.IsFailure)
                    return Result.Failure<(StockBalance, IReadOnlyList<BatchAllocation>)>(decreaseBatch.Error!);
                allocations.Add(new BatchAllocation(batch.Id, batch.BatchNumber, batch.ExpiryDate, take));
                remaining -= take;
            }

            if (remaining > 0)
                return Result.Failure<(StockBalance, IReadOnlyList<BatchAllocation>)>("Insufficient available non-expired batch stock.");
        }

        var decrease = balance.Decrease(quantity);
        if (decrease.IsFailure) return Result.Failure<(StockBalance, IReadOnlyList<BatchAllocation>)>(decrease.Error!);

        await PublishAvailabilityAsync(item, balance, cancellationToken);

        if (balance.QuantityOnHand <= item.ReorderLevel)
        {
            await publisher.EnqueueAsync(new IntegrationEvent(
                Guid.NewGuid(),
                "PurchaseRequisitionRequested",
                "v1",
                DateTimeOffset.UtcNow,
                null,
                null,
                facilityId,
                item.Id.ToString(),
                JsonSerializer.Serialize(new
                {
                    SignalId = Guid.NewGuid(),
                    ItemId = item.Id,
                    StoreId = storeId,
                    SuggestedQty = Math.Max(item.ReorderLevel * 2 - balance.QuantityOnHand, 1),
                    item.Sku,
                    item.Name
                })), cancellationToken);
        }

        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(((StockBalance)balance, (IReadOnlyList<BatchAllocation>)allocations));
    }

    public Task<List<Item>> ListItemsAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.Items.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderBy(x => x.Sku).ToListAsync(cancellationToken);

    public Task<List<Batch>> ListBatchesAsync(Guid facilityId, Guid? itemId, Guid? storeId, CancellationToken cancellationToken = default)
    {
        var q = db.Batches.AsNoTracking().Where(x => x.FacilityId == facilityId);
        if (itemId is Guid iid) q = q.Where(x => x.ItemId == iid);
        if (storeId is Guid sid) q = q.Where(x => x.StoreId == sid);
        return q.OrderBy(x => x.ExpiryDate).ThenBy(x => x.BatchNumber).ToListAsync(cancellationToken);
    }

    private async Task PublishAvailabilityAsync(Item item, StockBalance balance, CancellationToken cancellationToken)
    {
        var payload = new StockAvailabilityChanged(item.Id, balance.StoreId, balance.QuantityOnHand, balance.QuantityOnHand <= item.ReorderLevel);
        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(),
            "StockAvailabilityChanged",
            "v1",
            DateTimeOffset.UtcNow,
            null,
            null,
            item.FacilityId,
            item.Id.ToString(),
            JsonSerializer.Serialize(payload)), cancellationToken);
    }
}
