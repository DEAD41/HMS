using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Integration;
using HealthcareERP.Modules.Hms.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class LisService(
    HmsDbContext db,
    BillingService billingService,
    ILabAnalyzerAdapter labAnalyzerAdapter,
    IIntegrationEventPublisher publisher,
    IAuditWriter auditWriter)
{
    public async Task<Result<LabOrder>> AcceptAsync(
        Guid facilityId,
        Guid patientId,
        string testCode,
        string testName,
        Guid? encounterId,
        decimal chargeAmount,
        string currency,
        CancellationToken cancellationToken = default)
    {
        var create = LabOrder.Accept(facilityId, patientId, testCode, testName, encounterId);
        if (create.IsFailure) return create;
        db.LabOrders.Add(create.Value!);

        if (chargeAmount > 0)
        {
            var charge = await billingService.PostChargeAsync(
                facilityId, patientId, "LAB", testName, chargeAmount, currency, create.Value!.Id, Guid.NewGuid(), cancellationToken);
            if (charge.IsFailure) return Result.Failure<LabOrder>(charge.Error!);
        }

        await auditWriter.WriteAsync("HMS", "AcceptLab", nameof(LabOrder), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<LabOrder>> CollectSampleAsync(Guid orderId, string? sampleId, CancellationToken cancellationToken = default)
    {
        var order = await db.LabOrders.FirstOrDefaultAsync(x => x.Id == orderId, cancellationToken);
        if (order is null) return Result.Failure<LabOrder>("Lab order not found.");
        var collect = order.CollectSample(sampleId);
        if (collect.IsFailure) return Result.Failure<LabOrder>(collect.Error!);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(order);
    }

    public async Task<Result<LabOrder>> ImportFromAdapterAsync(Guid orderId, string? rawPayload, CancellationToken cancellationToken = default)
    {
        var order = await db.LabOrders.FirstOrDefaultAsync(x => x.Id == orderId, cancellationToken);
        if (order is null) return Result.Failure<LabOrder>("Lab order not found.");

        var imported = await labAnalyzerAdapter.ImportAsync(order.TestCode, rawPayload, cancellationToken);
        if (!imported.Success)
            return Result.Failure<LabOrder>(imported.Error ?? "Analyzer import failed.");

        var apply = order.ImportFromAdapter(imported.ResultValue, imported.IsCritical, "StubLabAnalyzer");
        if (apply.IsFailure) return Result.Failure<LabOrder>(apply.Error!);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(order);
    }

    public async Task<Result<LabOrder>> FinalizeAsync(Guid orderId, string resultValue, bool isCritical, CancellationToken cancellationToken = default)
    {
        var order = await db.LabOrders.FirstOrDefaultAsync(x => x.Id == orderId, cancellationToken);
        if (order is null) return Result.Failure<LabOrder>("Lab order not found.");
        var finalize = order.Finalize(resultValue, isCritical);
        if (finalize.IsFailure) return Result.Failure<LabOrder>(finalize.Error!);

        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(), "LabResultPosted", "v1", DateTimeOffset.UtcNow, null, null, order.FacilityId, order.PatientId.ToString(),
            JsonSerializer.Serialize(new { order.Id, order.PatientId, order.TestCode, order.ResultValue, order.IsCritical, order.SampleId })), cancellationToken);

        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(order);
    }

    public Task<List<LabOrder>> ListAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.LabOrders.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderByDescending(x => x.CreatedAt).ToListAsync(cancellationToken);
}
