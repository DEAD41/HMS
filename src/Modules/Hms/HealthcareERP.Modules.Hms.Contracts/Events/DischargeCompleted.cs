namespace HealthcareERP.Modules.Hms.Contracts.Events;

public sealed record DischargeCompleted(Guid DischargeId, Guid AdmissionId, Guid PatientId, Guid FacilityId);
