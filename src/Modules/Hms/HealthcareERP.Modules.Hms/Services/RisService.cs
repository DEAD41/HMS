using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Integration;
using HealthcareERP.Modules.Hms.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class RisService(
    HmsDbContext db,
    BillingService billingService,
    IPacsAdapter pacsAdapter,
    IIntegrationEventPublisher publisher,
    IAuditWriter auditWriter)
{
    public async Task<Result<RadiologyOrder>> AcceptAsync(
        Guid facilityId,
        Guid patientId,
        string modality,
        string studyName,
        Guid? encounterId,
        decimal chargeAmount,
        string currency,
        CancellationToken cancellationToken = default)
    {
        var create = RadiologyOrder.Accept(facilityId, patientId, modality, studyName, encounterId);
        if (create.IsFailure) return create;
        db.RadiologyOrders.Add(create.Value!);

        if (chargeAmount > 0)
        {
            var charge = await billingService.PostChargeAsync(
                facilityId, patientId, "RAD", studyName, chargeAmount, currency, create.Value!.Id, Guid.NewGuid(), cancellationToken);
            if (charge.IsFailure) return Result.Failure<RadiologyOrder>(charge.Error!);
        }

        await auditWriter.WriteAsync("HMS", "AcceptRad", nameof(RadiologyOrder), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<RadiologyOrder>> AcquireFromAdapterAsync(Guid orderId, CancellationToken cancellationToken = default)
    {
        var order = await db.RadiologyOrders.FirstOrDefaultAsync(x => x.Id == orderId, cancellationToken);
        if (order is null) return Result.Failure<RadiologyOrder>("Radiology order not found.");

        var acquired = await pacsAdapter.AcquireAsync(order.AccessionNumber ?? order.Id.ToString("N"), order.Modality, cancellationToken);
        if (!acquired.Success)
            return Result.Failure<RadiologyOrder>(acquired.Error ?? "PACS acquire failed.");

        var apply = order.AcquireFromAdapter(acquired.StudyInstanceUid, "StubPacs");
        if (apply.IsFailure) return Result.Failure<RadiologyOrder>(apply.Error!);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(order);
    }

    public async Task<Result<RadiologyOrder>> SignReportAsync(Guid orderId, string reportText, CancellationToken cancellationToken = default)
    {
        var order = await db.RadiologyOrders.FirstOrDefaultAsync(x => x.Id == orderId, cancellationToken);
        if (order is null) return Result.Failure<RadiologyOrder>("Radiology order not found.");
        var sign = order.SignReport(reportText);
        if (sign.IsFailure) return Result.Failure<RadiologyOrder>(sign.Error!);

        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(), "RadiologyReportPosted", "v1", DateTimeOffset.UtcNow, null, null, order.FacilityId, order.PatientId.ToString(),
            JsonSerializer.Serialize(new { order.Id, order.PatientId, order.Modality, order.AccessionNumber, order.StudyInstanceUid })), cancellationToken);

        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(order);
    }
}
