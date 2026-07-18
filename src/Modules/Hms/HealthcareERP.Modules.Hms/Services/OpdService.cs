using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class OpdService(HmsDbContext db, BillingService billingService, IAuditWriter auditWriter)
{
    public async Task<Result<OpdEncounter>> OpenAsync(
        Guid facilityId,
        Guid patientId,
        Guid clinicianEmployeeId,
        Guid? appointmentId,
        string? chiefComplaint,
        CancellationToken cancellationToken = default)
    {
        if (!await db.Patients.AnyAsync(x => x.Id == patientId, cancellationToken))
            return Result.Failure<OpdEncounter>("Patient not found.");

        if (appointmentId is Guid apptId)
        {
            var appt = await db.Appointments.FirstOrDefaultAsync(x => x.Id == apptId, cancellationToken);
            if (appt is null) return Result.Failure<OpdEncounter>("Appointment not found.");
            if (appt.Status != "CheckedIn" && appt.Status != "InProgress")
                return Result.Failure<OpdEncounter>("Appointment must be checked in.");
        }

        var create = OpdEncounter.Open(facilityId, patientId, clinicianEmployeeId, appointmentId, chiefComplaint);
        db.OpdEncounters.Add(create.Value!);
        await auditWriter.WriteAsync("HMS", "Open", nameof(OpdEncounter), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<OpdEncounter>> CloseAsync(Guid encounterId, string disposition, decimal consultationFee, string currency, CancellationToken cancellationToken = default)
    {
        var encounter = await db.OpdEncounters.FirstOrDefaultAsync(x => x.Id == encounterId, cancellationToken);
        if (encounter is null) return Result.Failure<OpdEncounter>("Encounter not found.");

        var close = encounter.Close(disposition);
        if (close.IsFailure) return Result.Failure<OpdEncounter>(close.Error!);

        if (consultationFee > 0)
        {
            var charge = await billingService.PostChargeAsync(
                encounter.FacilityId,
                encounter.PatientId,
                "OPDCONSULT",
                "OPD Consultation",
                consultationFee,
                currency,
                encounter.Id,
                Guid.NewGuid(),
                cancellationToken);
            if (charge.IsFailure) return Result.Failure<OpdEncounter>(charge.Error!);
        }

        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(encounter);
    }
}
