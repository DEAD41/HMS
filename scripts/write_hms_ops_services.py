#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def w(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print("wrote", rel)


w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Services/IpdService.cs",
    """
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
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Services/EmergencyService.cs",
    """
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
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Services/OtService.cs",
    """
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class OtService(HmsDbContext db, BillingService billingService, IAuditWriter auditWriter)
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
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Services/LisService.cs",
    """
using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class LisService(HmsDbContext db, BillingService billingService, IIntegrationEventPublisher publisher, IAuditWriter auditWriter)
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

    public async Task<Result<LabOrder>> FinalizeAsync(Guid orderId, string resultValue, bool isCritical, CancellationToken cancellationToken = default)
    {
        var order = await db.LabOrders.FirstOrDefaultAsync(x => x.Id == orderId, cancellationToken);
        if (order is null) return Result.Failure<LabOrder>("Lab order not found.");
        var finalize = order.Finalize(resultValue, isCritical);
        if (finalize.IsFailure) return Result.Failure<LabOrder>(finalize.Error!);

        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(), "LabResultPosted", "v1", DateTimeOffset.UtcNow, null, null, order.FacilityId, order.PatientId.ToString(),
            JsonSerializer.Serialize(new { order.Id, order.PatientId, order.TestCode, order.ResultValue, order.IsCritical })), cancellationToken);

        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(order);
    }

    public Task<List<LabOrder>> ListAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.LabOrders.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderByDescending(x => x.CreatedAt).ToListAsync(cancellationToken);
}
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Services/RisService.cs",
    """
using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class RisService(HmsDbContext db, BillingService billingService, IIntegrationEventPublisher publisher, IAuditWriter auditWriter)
{
    public async Task<Result<RadiologyOrder>> AcceptAsync(
        Guid facilityId,
        Guid patientId,
        string modality,
        string studyName,
        Guid? encounterId,
        decimal chargeAmount,
        string currency,
        CancellationToken cancellationToken = default)
    {
        var create = RadiologyOrder.Accept(facilityId, patientId, modality, studyName, encounterId);
        if (create.IsFailure) return create;
        db.RadiologyOrders.Add(create.Value!);

        if (chargeAmount > 0)
        {
            var charge = await billingService.PostChargeAsync(
                facilityId, patientId, "RAD", studyName, chargeAmount, currency, create.Value!.Id, Guid.NewGuid(), cancellationToken);
            if (charge.IsFailure) return Result.Failure<RadiologyOrder>(charge.Error!);
        }

        await auditWriter.WriteAsync("HMS", "AcceptRad", nameof(RadiologyOrder), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<RadiologyOrder>> SignReportAsync(Guid orderId, string reportText, CancellationToken cancellationToken = default)
    {
        var order = await db.RadiologyOrders.FirstOrDefaultAsync(x => x.Id == orderId, cancellationToken);
        if (order is null) return Result.Failure<RadiologyOrder>("Radiology order not found.");
        var sign = order.SignReport(reportText);
        if (sign.IsFailure) return Result.Failure<RadiologyOrder>(sign.Error!);

        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(), "RadiologyReportPosted", "v1", DateTimeOffset.UtcNow, null, null, order.FacilityId, order.PatientId.ToString(),
            JsonSerializer.Serialize(new { order.Id, order.PatientId, order.Modality, order.AccessionNumber })), cancellationToken);

        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(order);
    }
}
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Services/PharmacyService.cs",
    """
using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Contracts.Events;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Persistence;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class PharmacyService(HmsDbContext db, BillingService billingService, IIntegrationEventPublisher publisher, IAuditWriter auditWriter)
{
    public async Task<Result<MedicationDispense>> DispenseAsync(
        Guid facilityId,
        Guid patientId,
        Guid itemId,
        Guid storeId,
        string medicationName,
        decimal quantity,
        decimal unitPrice,
        string currency,
        Guid? encounterId,
        CancellationToken cancellationToken = default)
    {
        var create = MedicationDispense.Post(facilityId, patientId, itemId, storeId, medicationName, quantity, encounterId);
        if (create.IsFailure) return create;

        db.MedicationDispenses.Add(create.Value!);

        var payload = new MedicationDispensed(
            create.Value!.Id, facilityId, patientId, itemId, storeId, quantity, medicationName);
        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(), "MedicationDispensed", "v1", DateTimeOffset.UtcNow, null, null, facilityId, itemId.ToString(),
            JsonSerializer.Serialize(payload)), cancellationToken);

        var amount = unitPrice * quantity;
        if (amount > 0)
        {
            var charge = await billingService.PostChargeAsync(
                facilityId, patientId, "MED", medicationName, amount, currency, encounterId, create.Value.Id, cancellationToken);
            if (charge.IsFailure) return Result.Failure<MedicationDispense>(charge.Error!);
        }

        await auditWriter.WriteAsync("HMS", "Dispense", nameof(MedicationDispense), create.Value.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }
}
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Services/DischargeService.cs",
    """
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
""",
)

w(
    "src/Modules/Inventory/HealthcareERP.Modules.Inventory/Integration/MedicationDispensedHandler.cs",
    """
using System.Text.Json;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Infrastructure.Outbox;
using HealthcareERP.Modules.Inventory.Services;

namespace HealthcareERP.Modules.Inventory.Integration;

public sealed class MedicationDispensedHandler(InventoryService inventoryService) : IIntegrationEventHandler
{
    public string EventType => "MedicationDispensed";

    public async Task HandleAsync(IntegrationEvent integrationEvent, CancellationToken cancellationToken = default)
    {
        using var doc = JsonDocument.Parse(integrationEvent.PayloadJson);
        var root = doc.RootElement;
        var itemId = root.GetProperty("ItemId").GetGuid();
        var storeId = root.GetProperty("StoreId").GetGuid();
        var quantity = root.GetProperty("Quantity").GetDecimal();

        var result = await inventoryService.IssueAsync(
            integrationEvent.FacilityId,
            storeId,
            itemId,
            quantity,
            cancellationToken);

        if (result.IsFailure)
            throw new InvalidOperationException(result.Error);
    }
}
""",
)

print("services written")
