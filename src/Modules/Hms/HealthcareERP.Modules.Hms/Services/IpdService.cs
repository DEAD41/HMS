using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class IpdService(HmsDbContext db, BillingService billingService, IIntegrationEventPublisher publisher, IAuditWriter auditWriter)
{
    public async Task<Result<Bed>> CreateBedAsync(Guid facilityId, string code, string ward, string bedClass, CancellationToken cancellationToken = default)
    {
        if (await db.Beds.AnyAsync(x => x.FacilityId == facilityId && x.Code == code.Trim().ToUpperInvariant(), cancellationToken))
            return Result.Failure<Bed>("Bed code already exists.");

        var create = Bed.Create(facilityId, code, ward, bedClass);
        if (create.IsFailure) return create;
        db.Beds.Add(create.Value!);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public Task<List<Bed>> ListBedsAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.Beds.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderBy(x => x.Code).ToListAsync(cancellationToken);

    public async Task<Result<Admission>> AdmitAsync(
        Guid facilityId,
        Guid patientId,
        Guid attendingClinicianId,
        Guid bedId,
        string admittingDiagnosis,
        decimal dailyBedCharge,
        string currency,
        CancellationToken cancellationToken = default)
    {
        if (!await db.Patients.AnyAsync(x => x.Id == patientId && x.FacilityId == facilityId, cancellationToken))
            return Result.Failure<Admission>("Patient not found.");

        var bed = await db.Beds.FirstOrDefaultAsync(x => x.Id == bedId && x.FacilityId == facilityId, cancellationToken);
        if (bed is null) return Result.Failure<Admission>("Bed not found.");

        var occupy = bed.Occupy();
        if (occupy.IsFailure) return Result.Failure<Admission>(occupy.Error!);

        var admit = Admission.Admit(facilityId, patientId, attendingClinicianId, bedId, admittingDiagnosis);
        if (admit.IsFailure) return admit;

        db.Admissions.Add(admit.Value!);
        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(), "PatientAdmitted", "v1", DateTimeOffset.UtcNow, null, null, facilityId, patientId.ToString(),
            JsonSerializer.Serialize(new { admit.Value!.Id, PatientId = patientId, BedId = bedId })), cancellationToken);

        if (dailyBedCharge > 0)
        {
            var charge = await billingService.PostChargeAsync(
                facilityId, patientId, "BEDDAY", $"Bed charge {bed.BedClass}", dailyBedCharge, currency,
                admit.Value.Id, Guid.NewGuid(), cancellationToken);
            if (charge.IsFailure) return Result.Failure<Admission>(charge.Error!);
        }

        await auditWriter.WriteAsync("HMS", "Admit", nameof(Admission), admit.Value.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return admit;
    }

    public Task<List<Admission>> ListAdmissionsAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.Admissions.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderByDescending(x => x.CreatedAt).ToListAsync(cancellationToken);
}
