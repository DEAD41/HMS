using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Persistence;
using HealthcareERP.Modules.Hris.Contracts;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class OtService(HmsDbContext db, BillingService billingService, ICredentialStatusQuery credentialStatusQuery, IAuditWriter auditWriter)
{
    public async Task<Result<OtCase>> ScheduleAsync(
        Guid facilityId,
        Guid patientId,
        Guid surgeonEmployeeId,
        string theatreCode,
        string procedureName,
        DateTimeOffset scheduledAt,
        CancellationToken cancellationToken = default)
    {
        if (!await db.Patients.AnyAsync(x => x.Id == patientId, cancellationToken))
            return Result.Failure<OtCase>("Patient not found.");

        if (!await credentialStatusQuery.IsClinicianSchedulableAsync(surgeonEmployeeId, facilityId, cancellationToken))
            return Result.Failure<OtCase>("Surgeon is not credentialed for OT scheduling.");

        var overlap = await db.OtCases.AnyAsync(x =>
            x.TheatreCode == theatreCode.Trim().ToUpperInvariant() &&
            x.Status != "Cancelled" &&
            x.Status != "Completed" &&
            x.ScheduledAt == scheduledAt, cancellationToken);
        if (overlap) return Result.Failure<OtCase>("Theatre slot conflict.");

        var create = OtCase.Schedule(facilityId, patientId, surgeonEmployeeId, theatreCode, procedureName, scheduledAt);
        if (create.IsFailure) return create;
        db.OtCases.Add(create.Value!);
        await auditWriter.WriteAsync("HMS", "ScheduleOT", nameof(OtCase), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<OtCase>> CompleteChecklistAsync(Guid caseId, CancellationToken cancellationToken = default)
    {
        var otCase = await db.OtCases.FirstOrDefaultAsync(x => x.Id == caseId, cancellationToken);
        if (otCase is null) return Result.Failure<OtCase>("OT case not found.");
        var result = otCase.CompleteChecklist();
        if (result.IsFailure) return Result.Failure<OtCase>(result.Error!);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(otCase);
    }

    public async Task<Result<OtCase>> CompleteAsync(Guid caseId, decimal procedureFee, string currency, CancellationToken cancellationToken = default)
    {
        var otCase = await db.OtCases.FirstOrDefaultAsync(x => x.Id == caseId, cancellationToken);
        if (otCase is null) return Result.Failure<OtCase>("OT case not found.");
        var complete = otCase.Complete();
        if (complete.IsFailure) return Result.Failure<OtCase>(complete.Error!);

        if (procedureFee > 0)
        {
            var charge = await billingService.PostChargeAsync(
                otCase.FacilityId, otCase.PatientId, "OTPROC", otCase.ProcedureName, procedureFee, currency,
                otCase.Id, Guid.NewGuid(), cancellationToken);
            if (charge.IsFailure) return Result.Failure<OtCase>(charge.Error!);
        }

        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(otCase);
    }
}
