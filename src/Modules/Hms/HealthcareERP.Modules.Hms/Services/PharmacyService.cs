using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Contracts.Events;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Persistence;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class PharmacyService(HmsDbContext db, BillingService billingService, IIntegrationEventPublisher publisher, IAuditWriter auditWriter)
{
    public async Task<Result<MedicationDispense>> DispenseAsync(
        Guid facilityId,
        Guid patientId,
        Guid itemId,
        Guid storeId,
        string medicationName,
        decimal quantity,
        decimal unitPrice,
        string currency,
        Guid? encounterId,
        CancellationToken cancellationToken = default)
    {
        var create = MedicationDispense.Post(facilityId, patientId, itemId, storeId, medicationName, quantity, encounterId);
        if (create.IsFailure) return create;

        db.MedicationDispenses.Add(create.Value!);

        var payload = new MedicationDispensed(
            create.Value!.Id, facilityId, patientId, itemId, storeId, quantity, medicationName);
        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(), "MedicationDispensed", "v1", DateTimeOffset.UtcNow, null, null, facilityId, itemId.ToString(),
            JsonSerializer.Serialize(payload)), cancellationToken);

        var amount = unitPrice * quantity;
        if (amount > 0)
        {
            var charge = await billingService.PostChargeAsync(
                facilityId, patientId, "MED", medicationName, amount, currency, encounterId, create.Value.Id, cancellationToken);
            if (charge.IsFailure) return Result.Failure<MedicationDispense>(charge.Error!);
        }

        await auditWriter.WriteAsync("HMS", "Dispense", nameof(MedicationDispense), create.Value.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }
}
