using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Procurement.Contracts.Events;
using HealthcareERP.Modules.Procurement.Domain;
using HealthcareERP.Modules.Procurement.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Procurement.Services;

public sealed class ProcurementService(
    ProcurementDbContext db,
    IIntegrationEventPublisher publisher,
    IAuditWriter auditWriter)
{
    public async Task<Result<Vendor>> CreateVendorAsync(Guid facilityId, string code, string name, CancellationToken cancellationToken = default)
    {
        if (await db.Vendors.AnyAsync(x => x.FacilityId == facilityId && x.Code == code.Trim().ToUpperInvariant(), cancellationToken))
            return Result.Failure<Vendor>("Vendor code already exists.");

        var create = Vendor.Create(facilityId, code, name);
        if (create.IsFailure) return create;
        db.Vendors.Add(create.Value!);
        await auditWriter.WriteAsync("PRC", "Create", nameof(Vendor), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<PurchaseRequisition>> CreateRequisitionFromSignalAsync(
        Guid facilityId,
        Guid signalId,
        Guid itemId,
        Guid storeId,
        decimal quantity,
        string description,
        CancellationToken cancellationToken = default)
    {
        var existing = await db.PurchaseRequisitions.FirstOrDefaultAsync(x => x.SignalId == signalId, cancellationToken);
        if (existing is not null) return Result.Success(existing);

        var open = await db.PurchaseRequisitions.AnyAsync(x =>
            x.ItemId == itemId &&
            x.StoreId == storeId &&
            (x.Status == "Approved" || x.Status == "Draft"), cancellationToken);
        if (open) return Result.Failure<PurchaseRequisition>("Open requisition already exists for item/store.");

        var create = PurchaseRequisition.Create(facilityId, description, quantity, itemId, storeId, signalId);
        if (create.IsFailure) return create;
        db.PurchaseRequisitions.Add(create.Value!);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<PurchaseOrder>> IssuePurchaseOrderAsync(
        Guid facilityId,
        Guid vendorId,
        Guid? requisitionId,
        Guid? itemId,
        decimal quantity,
        decimal unitPrice,
        string currency,
        CancellationToken cancellationToken = default)
    {
        if (!await db.Vendors.AnyAsync(x => x.Id == vendorId && x.Status == "Active", cancellationToken))
            return Result.Failure<PurchaseOrder>("Active vendor required.");

        var create = PurchaseOrder.Issue(facilityId, vendorId, quantity, unitPrice, currency, requisitionId, itemId);
        if (create.IsFailure) return create;
        db.PurchaseOrders.Add(create.Value!);

        var payload = new PurchaseOrderIssued(create.Value!.Id, vendorId, facilityId, create.Value.TotalAmount);
        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(),
            "PurchaseOrderIssued",
            "v1",
            DateTimeOffset.UtcNow,
            null,
            null,
            facilityId,
            create.Value.Id.ToString(),
            JsonSerializer.Serialize(payload)), cancellationToken);

        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public Task<List<Vendor>> ListVendorsAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.Vendors.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderBy(x => x.Code).ToListAsync(cancellationToken);

    public Task<List<PurchaseRequisition>> ListRequisitionsAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.PurchaseRequisitions.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderByDescending(x => x.CreatedAt).ToListAsync(cancellationToken);
}
