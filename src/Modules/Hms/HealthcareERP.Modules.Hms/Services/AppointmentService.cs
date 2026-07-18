using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Persistence;
using HealthcareERP.Modules.Hris.Contracts;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class AppointmentService(HmsDbContext db, ICredentialStatusQuery credentialStatusQuery, IAuditWriter auditWriter)
{
    public async Task<Result<Appointment>> ScheduleAsync(
        Guid facilityId,
        Guid patientId,
        Guid clinicianEmployeeId,
        DateTimeOffset startsAt,
        DateTimeOffset endsAt,
        Guid? clinicOrgUnitId,
        string? reason,
        CancellationToken cancellationToken = default)
    {
        if (!await db.Patients.AnyAsync(x => x.Id == patientId && x.FacilityId == facilityId, cancellationToken))
            return Result.Failure<Appointment>("Patient not found.");

        if (!await credentialStatusQuery.IsClinicianSchedulableAsync(clinicianEmployeeId, facilityId, cancellationToken))
            return Result.Failure<Appointment>("Clinician is not credentialed for scheduling.");

        var overlap = await db.Appointments.AnyAsync(x =>
            x.ClinicianEmployeeId == clinicianEmployeeId &&
            x.Status != "Cancelled" &&
            x.StartsAt < endsAt &&
            startsAt < x.EndsAt, cancellationToken);
        if (overlap) return Result.Failure<Appointment>("Clinician has a conflicting appointment.");

        var create = Appointment.Schedule(facilityId, patientId, clinicianEmployeeId, startsAt, endsAt, clinicOrgUnitId, reason);
        if (create.IsFailure) return create;

        db.Appointments.Add(create.Value!);
        await auditWriter.WriteAsync("HMS", "Schedule", nameof(Appointment), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<Appointment>> CheckInAsync(Guid appointmentId, CancellationToken cancellationToken = default)
    {
        var appointment = await db.Appointments.FirstOrDefaultAsync(x => x.Id == appointmentId, cancellationToken);
        if (appointment is null) return Result.Failure<Appointment>("Appointment not found.");
        var result = appointment.CheckIn();
        if (result.IsFailure) return Result.Failure<Appointment>(result.Error!);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(appointment);
    }

    public Task<List<Appointment>> ListAsync(Guid facilityId, DateOnly date, CancellationToken cancellationToken = default)
    {
        var start = date.ToDateTime(TimeOnly.MinValue, DateTimeKind.Utc);
        var end = date.ToDateTime(TimeOnly.MaxValue, DateTimeKind.Utc);
        return db.Appointments.AsNoTracking()
            .Where(x => x.FacilityId == facilityId && x.StartsAt >= start && x.StartsAt <= end)
            .OrderBy(x => x.StartsAt)
            .ToListAsync(cancellationToken);
    }
}
