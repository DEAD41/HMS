using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hris.Contracts.Events;
using HealthcareERP.Modules.Hris.Domain;
using HealthcareERP.Modules.Hris.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hris.Services;

public sealed class PayrollService(HrisDbContext db, IIntegrationEventPublisher publisher, IAuditWriter auditWriter)
{
    public async Task<Result<PayrollRun>> CreateAsync(
        Guid facilityId,
        string period,
        decimal grossAmount,
        decimal deductions,
        CancellationToken cancellationToken = default)
    {
        if (await db.PayrollRuns.AnyAsync(x => x.FacilityId == facilityId && x.Period == period.Trim(), cancellationToken))
            return Result.Failure<PayrollRun>("Payroll period already exists.");

        var create = PayrollRun.Create(facilityId, period, grossAmount, deductions);
        if (create.IsFailure) return create;
        db.PayrollRuns.Add(create.Value!);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<PayrollRun>> PostAsync(Guid payrollRunId, CancellationToken cancellationToken = default)
    {
        var run = await db.PayrollRuns.FirstOrDefaultAsync(x => x.Id == payrollRunId, cancellationToken);
        if (run is null) return Result.Failure<PayrollRun>("Payroll run not found.");
        var post = run.Post();
        if (post.IsFailure) return Result.Failure<PayrollRun>(post.Error!);

        var payload = new PayrollPosted(run.Id, run.FacilityId, run.Period, run.GrossAmount, run.NetAmount);
        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(), "PayrollPosted", "v1", DateTimeOffset.UtcNow, null, null, run.FacilityId, run.Id.ToString(),
            JsonSerializer.Serialize(payload)), cancellationToken);

        await auditWriter.WriteAsync("HRIS", "PostPayroll", nameof(PayrollRun), run.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(run);
    }

    public Task<List<PayrollRun>> ListAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.PayrollRuns.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderByDescending(x => x.CreatedAt).ToListAsync(cancellationToken);
}
