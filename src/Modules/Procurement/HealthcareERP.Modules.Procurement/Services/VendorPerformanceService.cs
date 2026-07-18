using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Procurement.Domain;
using HealthcareERP.Modules.Procurement.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Procurement.Services;

public sealed class VendorPerformanceService(ProcurementDbContext db, IAuditWriter auditWriter)
{
    public async Task<Result<VendorScorecard>> PublishAsync(
        Guid facilityId,
        Guid vendorId,
        string period,
        CancellationToken cancellationToken = default)
    {
        if (!await db.Vendors.AnyAsync(x => x.Id == vendorId && x.FacilityId == facilityId, cancellationToken))
            return Result.Failure<VendorScorecard>("Vendor not found.");

        var orders = await db.PurchaseOrders.AsNoTracking()
            .Where(x => x.FacilityId == facilityId && x.VendorId == vendorId)
            .ToListAsync(cancellationToken);

        // MVP: derive synthetic on-time/quality from order volume until GRN/QC events exist.
        var count = orders.Count;
        var spend = orders.Sum(x => x.Quantity * x.UnitPrice);
        var onTime = count == 0 ? 100m : Math.Min(100m, 70m + count * 2m);
        var quality = count == 0 ? 100m : Math.Min(100m, 75m + count);

        var existing = await db.VendorScorecards.FirstOrDefaultAsync(
            x => x.FacilityId == facilityId && x.VendorId == vendorId && x.Period == period.Trim(), cancellationToken);
        if (existing is not null) db.VendorScorecards.Remove(existing);

        var create = VendorScorecard.Publish(facilityId, vendorId, period, count, spend, onTime, quality);
        if (create.IsFailure) return create;
        db.VendorScorecards.Add(create.Value!);
        await auditWriter.WriteAsync("PRC", "PublishScorecard", nameof(VendorScorecard), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public Task<List<VendorScorecard>> ListAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.VendorScorecards.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderByDescending(x => x.CreatedAt).ToListAsync(cancellationToken);

    public async Task<VendorScorecard?> GetForVendorAsync(Guid vendorId, CancellationToken cancellationToken = default) =>
        await db.VendorScorecards.AsNoTracking()
            .Where(x => x.VendorId == vendorId)
            .OrderByDescending(x => x.CreatedAt)
            .FirstOrDefaultAsync(cancellationToken);
}
