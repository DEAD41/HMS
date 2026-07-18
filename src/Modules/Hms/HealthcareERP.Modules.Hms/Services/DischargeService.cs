using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Contracts.Events;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class DischargeService(
    HmsDbContext db,
    AppointmentService appointmentService,
    IIntegrationEventPublisher publisher,
    IAuditWriter auditWriter)
{
    public async Task<Result<DischargeProcess>> CompleteAsync(
        Guid facilityId,
        Guid admissionId,
        string summary,
        bool scheduleFollowUp,
        Guid? clinicianEmployeeId,
        DateTimeOffset? followUpAt,
        CancellationToken cancellationToken = default)
    {
        var admission = await db.Admissions.FirstOrDefaultAsync(x => x.Id == admissionId && x.FacilityId == facilityId, cancellationToken);
        if (admission is null) return Result.Failure<DischargeProcess>("Admission not found.");
        if (admission.Status == "Discharged") return Result.Failure<DischargeProcess>("Already discharged.");

        var initiate = admission.InitiateDischarge();
        if (initiate.IsFailure) return Result.Failure<DischargeProcess>(initiate.Error!);

        Guid? followUpId = null;
        if (scheduleFollowUp)
        {
            if (clinicianEmployeeId is null || followUpAt is null)
                return Result.Failure<DischargeProcess>("Follow-up clinician and time are required.");
            var appt = await appointmentService.ScheduleAsync(
                facilityId,
                admission.PatientId,
                clinicianEmployeeId.Value,
                followUpAt.Value,
                followUpAt.Value.AddMinutes(30),
                null,
                "Post-discharge follow-up",
                cancellationToken);
            if (appt.IsFailure) return Result.Failure<DischargeProcess>(appt.Error!);
            followUpId = appt.Value!.Id;
        }

        var discharge = DischargeProcess.Initiate(facilityId, admission.PatientId, admissionId);
        if (discharge.IsFailure) return discharge;
        var complete = discharge.Value!.Complete(summary, followUpId);
        if (complete.IsFailure) return Result.Failure<DischargeProcess>(complete.Error!);

        var finish = admission.CompleteDischarge();
        if (finish.IsFailure) return Result.Failure<DischargeProcess>(finish.Error!);

        if (admission.BedId is Guid bedId)
        {
            var bed = await db.Beds.FirstOrDefaultAsync(x => x.Id == bedId, cancellationToken);
            if (bed is not null)
            {
                var release = bed.Release();
                if (release.IsFailure) return Result.Failure<DischargeProcess>(release.Error!);
            }
        }

        db.DischargeProcesses.Add(discharge.Value);
        var payload = new DischargeCompleted(discharge.Value.Id, admissionId, admission.PatientId, facilityId);
        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(), "DischargeCompleted", "v1", DateTimeOffset.UtcNow, null, null, facilityId, admission.PatientId.ToString(),
            JsonSerializer.Serialize(payload)), cancellationToken);

        await auditWriter.WriteAsync("HMS", "Discharge", nameof(DischargeProcess), discharge.Value.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return discharge;
    }
}
