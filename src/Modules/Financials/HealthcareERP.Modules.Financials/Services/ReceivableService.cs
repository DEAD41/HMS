using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Financials.Domain;
using HealthcareERP.Modules.Financials.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Financials.Services;

public sealed class ReceivableService(FinancialsDbContext db, IAuditWriter auditWriter)
{
    public async Task<Result<Receivable>> CreateFromChargeAsync(
        Guid facilityId,
        Guid patientId,
        Guid sourceChargeId,
        string chargeCode,
        decimal amount,
        string currency,
        CancellationToken cancellationToken = default)
    {
        var existing = await db.Receivables.FirstOrDefaultAsync(x => x.SourceChargeId == sourceChargeId, cancellationToken);
        if (existing is not null) return Result.Success(existing);

        var create = Receivable.FromCharge(facilityId, patientId, sourceChargeId, chargeCode, amount, currency);
        if (create.IsFailure) return create;
        db.Receivables.Add(create.Value!);
        await auditWriter.WriteAsync("FIN", "OpenReceivable", nameof(Receivable), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public Task<List<Receivable>> ListAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.Receivables.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderByDescending(x => x.CreatedAt).ToListAsync(cancellationToken);
}
