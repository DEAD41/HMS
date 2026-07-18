using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Contracts.Events;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class PatientService(HmsDbContext db, IIntegrationEventPublisher publisher, IAuditWriter auditWriter)
{
    public async Task<Result<Patient>> RegisterAsync(
        Guid facilityId,
        string mrn,
        string firstName,
        string lastName,
        DateOnly? dateOfBirth,
        string? phone,
        string? nationalId,
        CancellationToken cancellationToken = default)
    {
        if (await db.Patients.AnyAsync(x => x.FacilityId == facilityId && x.Mrn == mrn.Trim().ToUpperInvariant(), cancellationToken))
            return Result.Failure<Patient>("MRN already exists for facility.");

        var create = Patient.Register(facilityId, mrn, firstName, lastName, dateOfBirth, phone, nationalId);
        if (create.IsFailure) return create;

        var patient = create.Value!;
        db.Patients.Add(patient);

        var payload = new PatientChanged(patient.Id, patient.Mrn, patient.FullName, patient.Status);
        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(), "PatientChanged", "v1", DateTimeOffset.UtcNow, null, null, facilityId, patient.Id.ToString(),
            JsonSerializer.Serialize(payload)), cancellationToken);

        await auditWriter.WriteAsync("HMS", "Register", nameof(Patient), patient.Id, null, JsonSerializer.Serialize(payload), cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(patient);
    }

    public Task<List<Patient>> SearchAsync(Guid facilityId, string? query, CancellationToken cancellationToken = default)
    {
        var q = db.Patients.AsNoTracking().Where(x => x.FacilityId == facilityId);
        if (!string.IsNullOrWhiteSpace(query))
        {
            var term = query.Trim().ToUpperInvariant();
            q = q.Where(x => x.Mrn.Contains(term) || x.FirstName.ToUpper().Contains(term) || x.LastName.ToUpper().Contains(term));
        }
        return q.OrderBy(x => x.Mrn).Take(50).ToListAsync(cancellationToken);
    }
}
