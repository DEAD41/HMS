using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class BillingService(HmsDbContext db, IIntegrationEventPublisher publisher, IAuditWriter auditWriter)
{
    public async Task<Result<Charge>> PostChargeAsync(
        Guid facilityId,
        Guid patientId,
        string chargeCode,
        string description,
        decimal amount,
        string currency,
        Guid? encounterId,
        Guid? sourceEventId,
        CancellationToken cancellationToken = default)
    {
        if (sourceEventId is Guid sid && await db.Charges.AnyAsync(x => x.SourceEventId == sid, cancellationToken))
        {
            var existing = await db.Charges.FirstAsync(x => x.SourceEventId == sid, cancellationToken);
            return Result.Success(existing);
        }

        var create = Charge.Create(facilityId, patientId, chargeCode, description, amount, currency, encounterId, sourceEventId);
        if (create.IsFailure) return create;

        db.Charges.Add(create.Value!);
        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(),
            "BillableEventCreated",
            "v1",
            DateTimeOffset.UtcNow,
            null,
            sourceEventId,
            facilityId,
            patientId.ToString(),
            JsonSerializer.Serialize(new
            {
                create.Value!.Id,
                create.Value.PatientId,
                create.Value.ChargeCode,
                create.Value.Amount,
                create.Value.Currency
            })), cancellationToken);

        await auditWriter.WriteAsync("HMS", "PostCharge", nameof(Charge), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public Task<List<Charge>> ListForPatientAsync(Guid patientId, CancellationToken cancellationToken = default) =>
        db.Charges.AsNoTracking().Where(x => x.PatientId == patientId).OrderByDescending(x => x.CreatedAt).ToListAsync(cancellationToken);
}
