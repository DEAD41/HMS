using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Contracts.Events;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Persistence;
using HealthcareERP.Modules.Hris.Contracts;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class NursingService(
    HmsDbContext db,
    ICredentialStatusQuery credentialStatusQuery,
    IIntegrationEventPublisher publisher,
    IAuditWriter auditWriter)
{
    public async Task<Result<NursingCarePlan>> CreateCarePlanAsync(
        Guid facilityId,
        Guid admissionId,
        string summary,
        string goals,
        CancellationToken cancellationToken = default)
    {
        var admission = await db.Admissions.AsNoTracking()
            .FirstOrDefaultAsync(x => x.Id == admissionId && x.FacilityId == facilityId, cancellationToken);
        if (admission is null) return Result.Failure<NursingCarePlan>("Admission not found.");
        if (admission.Status is "Discharged")
            return Result.Failure<NursingCarePlan>("Cannot create care plan for discharged admission.");

        var create = NursingCarePlan.Create(facilityId, admissionId, admission.PatientId, summary, goals);
        if (create.IsFailure) return create;
        db.NursingCarePlans.Add(create.Value!);
        await auditWriter.WriteAsync("HMS", "CreateCarePlan", nameof(NursingCarePlan), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public Task<List<NursingCarePlan>> ListCarePlansAsync(Guid admissionId, CancellationToken cancellationToken = default) =>
        db.NursingCarePlans.AsNoTracking().Where(x => x.AdmissionId == admissionId).OrderByDescending(x => x.CreatedAt).ToListAsync(cancellationToken);

    public async Task<Result<MarEntry>> RecordMarAsync(
        Guid facilityId,
        Guid admissionId,
        Guid medicationDispenseId,
        Guid nurseEmployeeId,
        string doseInstanceId,
        string action,
        string? notes,
        CancellationToken cancellationToken = default)
    {
        var admission = await db.Admissions.AsNoTracking()
            .FirstOrDefaultAsync(x => x.Id == admissionId && x.FacilityId == facilityId, cancellationToken);
        if (admission is null) return Result.Failure<MarEntry>("Admission not found.");

        if (!await credentialStatusQuery.IsNurseCapableAsync(nurseEmployeeId, facilityId, cancellationToken))
            return Result.Failure<MarEntry>("Nurse is not credentialed for medication administration.");

        var dispense = await db.MedicationDispenses.AsNoTracking()
            .FirstOrDefaultAsync(x => x.Id == medicationDispenseId && x.FacilityId == facilityId && x.PatientId == admission.PatientId, cancellationToken);
        if (dispense is null) return Result.Failure<MarEntry>("Medication dispense not found for patient.");

        var existing = await db.MarEntries.FirstOrDefaultAsync(x =>
            x.AdmissionId == admissionId &&
            x.DoseInstanceId == doseInstanceId.Trim(), cancellationToken);

        if (existing is null)
        {
            var create = MarEntry.Schedule(
                facilityId, admissionId, admission.PatientId, medicationDispenseId,
                nurseEmployeeId, doseInstanceId, dispense.MedicationName);
            if (create.IsFailure) return create;
            existing = create.Value!;
            db.MarEntries.Add(existing);
        }
        else if (existing.Status == "Administered")
        {
            return Result.Failure<MarEntry>("MAR dose already administered and cannot be changed.");
        }

        var normalized = action.Trim().ToLowerInvariant();
        var apply = normalized switch
        {
            "administer" or "administered" => existing.Administer(notes),
            "hold" or "held" => existing.Hold(notes),
            "refuse" or "refused" => existing.Refuse(notes),
            "miss" or "missed" => existing.Miss(notes),
            _ => Result.Failure("Unknown MAR action. Use administer|hold|refuse|miss.")
        };
        if (apply.IsFailure) return Result.Failure<MarEntry>(apply.Error!);

        if (existing.Status == "Administered")
        {
            var payload = new MarAdministered(
                existing.Id, facilityId, admissionId, admission.PatientId,
                medicationDispenseId, nurseEmployeeId, existing.DoseInstanceId);
            await publisher.EnqueueAsync(new IntegrationEvent(
                Guid.NewGuid(), "MarAdministered", "v1", DateTimeOffset.UtcNow, null, null, facilityId, admission.PatientId.ToString(),
                JsonSerializer.Serialize(payload)), cancellationToken);
        }

        await auditWriter.WriteAsync("HMS", "RecordMar", nameof(MarEntry), existing.Id, null, existing.Status, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(existing);
    }

    public Task<List<MarEntry>> ListMarAsync(Guid admissionId, CancellationToken cancellationToken = default) =>
        db.MarEntries.AsNoTracking().Where(x => x.AdmissionId == admissionId).OrderByDescending(x => x.CreatedAt).ToListAsync(cancellationToken);
}
