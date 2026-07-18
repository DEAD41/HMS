namespace HealthcareERP.Modules.Hms.Contracts.Events;

public sealed record MarAdministered(
    Guid MarEntryId,
    Guid FacilityId,
    Guid AdmissionId,
    Guid PatientId,
    Guid MedicationDispenseId,
    Guid NurseEmployeeId,
    string DoseInstanceId);
