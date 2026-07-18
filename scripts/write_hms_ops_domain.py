#!/usr/bin/env python3
"""Generate HMS operational Increment 3 sources."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def w(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print("wrote", rel)


# ---- Domain ----
w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Domain/Bed.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class Bed : AggregateRoot
{
    private Bed() { }

    public Guid FacilityId { get; private set; }
    public string Code { get; private set; } = string.Empty;
    public string Ward { get; private set; } = string.Empty;
    public string BedClass { get; private set; } = "General";
    public string Status { get; private set; } = "Available";

    public static Result<Bed> Create(Guid facilityId, string code, string ward, string bedClass)
    {
        if (facilityId == Guid.Empty) return Result.Failure<Bed>("Facility is required.");
        if (string.IsNullOrWhiteSpace(code)) return Result.Failure<Bed>("Bed code is required.");
        return Result.Success(new Bed
        {
            FacilityId = facilityId,
            Code = code.Trim().ToUpperInvariant(),
            Ward = ward.Trim(),
            BedClass = string.IsNullOrWhiteSpace(bedClass) ? "General" : bedClass.Trim(),
            Status = "Available"
        });
    }

    public Result Occupy()
    {
        if (Status != "Available") return Result.Failure("Bed is not available.");
        Status = "Occupied";
        Touch();
        return Result.Success();
    }

    public Result Release()
    {
        if (Status != "Occupied" && Status != "Blocked") return Result.Failure("Bed is not occupied.");
        Status = "Available";
        Touch();
        return Result.Success();
    }
}
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Domain/Admission.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class Admission : AggregateRoot
{
    private Admission() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid AttendingClinicianId { get; private set; }
    public Guid? BedId { get; private set; }
    public string AdmittingDiagnosis { get; private set; } = string.Empty;
    public string Status { get; private set; } = "Admitted";

    public static Result<Admission> Admit(
        Guid facilityId,
        Guid patientId,
        Guid attendingClinicianId,
        Guid bedId,
        string admittingDiagnosis)
    {
        if (patientId == Guid.Empty || attendingClinicianId == Guid.Empty || bedId == Guid.Empty)
            return Result.Failure<Admission>("Patient, clinician, and bed are required.");
        if (string.IsNullOrWhiteSpace(admittingDiagnosis))
            return Result.Failure<Admission>("Admitting diagnosis is required.");

        return Result.Success(new Admission
        {
            FacilityId = facilityId,
            PatientId = patientId,
            AttendingClinicianId = attendingClinicianId,
            BedId = bedId,
            AdmittingDiagnosis = admittingDiagnosis.Trim(),
            Status = "Admitted"
        });
    }

    public Result InitiateDischarge()
    {
        if (Status != "Admitted" && Status != "Transferred")
            return Result.Failure("Admission is not active.");
        Status = "DischargeInitiated";
        Touch();
        return Result.Success();
    }

    public Result CompleteDischarge()
    {
        if (Status is not ("DischargeInitiated" or "Admitted"))
            return Result.Failure("Discharge cannot be completed from current status.");
        Status = "Discharged";
        Touch();
        return Result.Success();
    }
}
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Domain/ErEncounter.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class ErEncounter : AggregateRoot
{
    private ErEncounter() { }

    public Guid FacilityId { get; private set; }
    public Guid? PatientId { get; private set; }
    public string TemporaryId { get; private set; } = string.Empty;
    public string TriageCategory { get; private set; } = "Untriaged";
    public string Status { get; private set; } = "Arrived";
    public string? Disposition { get; private set; }

    public static Result<ErEncounter> Open(Guid facilityId, Guid? patientId, string? temporaryId)
    {
        if (facilityId == Guid.Empty) return Result.Failure<ErEncounter>("Facility is required.");
        if (patientId is null && string.IsNullOrWhiteSpace(temporaryId))
            return Result.Failure<ErEncounter>("Patient or temporary ID is required.");

        return Result.Success(new ErEncounter
        {
            FacilityId = facilityId,
            PatientId = patientId,
            TemporaryId = string.IsNullOrWhiteSpace(temporaryId)
                ? $"UNK-{DateTimeOffset.UtcNow:yyyyMMddHHmmss}"
                : temporaryId.Trim().ToUpperInvariant(),
            Status = "Arrived",
            TriageCategory = "Untriaged"
        });
    }

    public Result Triage(string category)
    {
        if (string.IsNullOrWhiteSpace(category)) return Result.Failure("Triage category is required.");
        TriageCategory = category.Trim();
        Status = "Triaged";
        Touch();
        return Result.Success();
    }

    public Result Dispose(string disposition)
    {
        if (string.IsNullOrWhiteSpace(disposition)) return Result.Failure("Disposition is required.");
        Disposition = disposition.Trim();
        Status = "Disposed";
        Touch();
        return Result.Success();
    }
}
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Domain/OtCase.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class OtCase : AggregateRoot
{
    private OtCase() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid SurgeonEmployeeId { get; private set; }
    public string TheatreCode { get; private set; } = string.Empty;
    public string ProcedureName { get; private set; } = string.Empty;
    public DateTimeOffset ScheduledAt { get; private set; }
    public bool ChecklistComplete { get; private set; }
    public string Status { get; private set; } = "Scheduled";

    public static Result<OtCase> Schedule(
        Guid facilityId,
        Guid patientId,
        Guid surgeonEmployeeId,
        string theatreCode,
        string procedureName,
        DateTimeOffset scheduledAt)
    {
        if (patientId == Guid.Empty || surgeonEmployeeId == Guid.Empty)
            return Result.Failure<OtCase>("Patient and surgeon are required.");
        if (string.IsNullOrWhiteSpace(theatreCode) || string.IsNullOrWhiteSpace(procedureName))
            return Result.Failure<OtCase>("Theatre and procedure are required.");

        return Result.Success(new OtCase
        {
            FacilityId = facilityId,
            PatientId = patientId,
            SurgeonEmployeeId = surgeonEmployeeId,
            TheatreCode = theatreCode.Trim().ToUpperInvariant(),
            ProcedureName = procedureName.Trim(),
            ScheduledAt = scheduledAt,
            Status = "Scheduled"
        });
    }

    public Result CompleteChecklist()
    {
        ChecklistComplete = true;
        Status = "PreOp";
        Touch();
        return Result.Success();
    }

    public Result Complete()
    {
        if (!ChecklistComplete) return Result.Failure("Pre-op checklist must be complete.");
        Status = "Completed";
        Touch();
        return Result.Success();
    }
}
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Domain/LabOrder.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class LabOrder : AggregateRoot
{
    private LabOrder() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid? EncounterId { get; private set; }
    public string TestCode { get; private set; } = string.Empty;
    public string TestName { get; private set; } = string.Empty;
    public string Status { get; private set; } = "Received";
    public string? ResultValue { get; private set; }
    public bool IsCritical { get; private set; }

    public static Result<LabOrder> Accept(Guid facilityId, Guid patientId, string testCode, string testName, Guid? encounterId)
    {
        if (string.IsNullOrWhiteSpace(testCode) || string.IsNullOrWhiteSpace(testName))
            return Result.Failure<LabOrder>("Test code and name are required.");
        return Result.Success(new LabOrder
        {
            FacilityId = facilityId,
            PatientId = patientId,
            EncounterId = encounterId,
            TestCode = testCode.Trim().ToUpperInvariant(),
            TestName = testName.Trim(),
            Status = "Received"
        });
    }

    public Result Finalize(string resultValue, bool isCritical)
    {
        if (string.IsNullOrWhiteSpace(resultValue)) return Result.Failure("Result value is required.");
        ResultValue = resultValue.Trim();
        IsCritical = isCritical;
        Status = "Final";
        Touch();
        return Result.Success();
    }
}
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Domain/RadiologyOrder.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class RadiologyOrder : AggregateRoot
{
    private RadiologyOrder() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid? EncounterId { get; private set; }
    public string Modality { get; private set; } = string.Empty;
    public string StudyName { get; private set; } = string.Empty;
    public string Status { get; private set; } = "Ordered";
    public string? ReportText { get; private set; }
    public string? AccessionNumber { get; private set; }

    public static Result<RadiologyOrder> Accept(
        Guid facilityId,
        Guid patientId,
        string modality,
        string studyName,
        Guid? encounterId)
    {
        if (string.IsNullOrWhiteSpace(modality) || string.IsNullOrWhiteSpace(studyName))
            return Result.Failure<RadiologyOrder>("Modality and study name are required.");
        return Result.Success(new RadiologyOrder
        {
            FacilityId = facilityId,
            PatientId = patientId,
            EncounterId = encounterId,
            Modality = modality.Trim().ToUpperInvariant(),
            StudyName = studyName.Trim(),
            Status = "Ordered",
            AccessionNumber = $"ACC-{Guid.NewGuid():N}"[..16].ToUpperInvariant()
        });
    }

    public Result SignReport(string reportText)
    {
        if (string.IsNullOrWhiteSpace(reportText)) return Result.Failure("Report text is required.");
        ReportText = reportText.Trim();
        Status = "Reported";
        Touch();
        return Result.Success();
    }
}
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Domain/MedicationDispense.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class MedicationDispense : AggregateRoot
{
    private MedicationDispense() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid? EncounterId { get; private set; }
    public Guid ItemId { get; private set; }
    public Guid StoreId { get; private set; }
    public string MedicationName { get; private set; } = string.Empty;
    public decimal Quantity { get; private set; }
    public string Status { get; private set; } = "Posted";

    public static Result<MedicationDispense> Post(
        Guid facilityId,
        Guid patientId,
        Guid itemId,
        Guid storeId,
        string medicationName,
        decimal quantity,
        Guid? encounterId)
    {
        if (quantity <= 0) return Result.Failure<MedicationDispense>("Quantity must be positive.");
        if (itemId == Guid.Empty || storeId == Guid.Empty)
            return Result.Failure<MedicationDispense>("Item and store are required.");
        if (string.IsNullOrWhiteSpace(medicationName))
            return Result.Failure<MedicationDispense>("Medication name is required.");

        return Result.Success(new MedicationDispense
        {
            FacilityId = facilityId,
            PatientId = patientId,
            EncounterId = encounterId,
            ItemId = itemId,
            StoreId = storeId,
            MedicationName = medicationName.Trim(),
            Quantity = quantity,
            Status = "Posted"
        });
    }
}
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Domain/DischargeProcess.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class DischargeProcess : AggregateRoot
{
    private DischargeProcess() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid AdmissionId { get; private set; }
    public string Summary { get; private set; } = string.Empty;
    public string Status { get; private set; } = "Initiated";
    public Guid? FollowUpAppointmentId { get; private set; }

    public static Result<DischargeProcess> Initiate(Guid facilityId, Guid patientId, Guid admissionId)
    {
        if (admissionId == Guid.Empty) return Result.Failure<DischargeProcess>("Admission is required.");
        return Result.Success(new DischargeProcess
        {
            FacilityId = facilityId,
            PatientId = patientId,
            AdmissionId = admissionId,
            Status = "Initiated"
        });
    }

    public Result Complete(string summary, Guid? followUpAppointmentId)
    {
        if (string.IsNullOrWhiteSpace(summary)) return Result.Failure("Discharge summary is required.");
        Summary = summary.Trim();
        FollowUpAppointmentId = followUpAppointmentId;
        Status = "Completed";
        Touch();
        return Result.Success();
    }
}
""",
)

# ---- Contracts ----
w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms.Contracts/Events/MedicationDispensed.cs",
    """
namespace HealthcareERP.Modules.Hms.Contracts.Events;

public sealed record MedicationDispensed(
    Guid DispenseId,
    Guid FacilityId,
    Guid PatientId,
    Guid ItemId,
    Guid StoreId,
    decimal Quantity,
    string MedicationName);
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms.Contracts/Events/DischargeCompleted.cs",
    """
namespace HealthcareERP.Modules.Hms.Contracts.Events;

public sealed record DischargeCompleted(Guid DischargeId, Guid AdmissionId, Guid PatientId, Guid FacilityId);
""",
)

print("domain written")
