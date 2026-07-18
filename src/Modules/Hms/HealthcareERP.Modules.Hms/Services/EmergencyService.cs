using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class EmergencyService(HmsDbContext db, IAuditWriter auditWriter)
{
    public async Task<Result<ErEncounter>> OpenAsync(Guid facilityId, Guid? patientId, string? temporaryId, CancellationToken cancellationToken = default)
    {
        var create = ErEncounter.Open(facilityId, patientId, temporaryId);
        if (create.IsFailure) return create;
        db.ErEncounters.Add(create.Value!);
        await auditWriter.WriteAsync("HMS", "OpenER", nameof(ErEncounter), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<ErEncounter>> TriageAsync(Guid encounterId, string category, CancellationToken cancellationToken = default)
    {
        var encounter = await db.ErEncounters.FirstOrDefaultAsync(x => x.Id == encounterId, cancellationToken);
        if (encounter is null) return Result.Failure<ErEncounter>("ER encounter not found.");
        var triage = encounter.Triage(category);
        if (triage.IsFailure) return Result.Failure<ErEncounter>(triage.Error!);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(encounter);
    }

    public async Task<Result<ErEncounter>> DisposeAsync(Guid encounterId, string disposition, CancellationToken cancellationToken = default)
    {
        var encounter = await db.ErEncounters.FirstOrDefaultAsync(x => x.Id == encounterId, cancellationToken);
        if (encounter is null) return Result.Failure<ErEncounter>("ER encounter not found.");
        var dispose = encounter.Dispose(disposition);
        if (dispose.IsFailure) return Result.Failure<ErEncounter>(dispose.Error!);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(encounter);
    }
}
