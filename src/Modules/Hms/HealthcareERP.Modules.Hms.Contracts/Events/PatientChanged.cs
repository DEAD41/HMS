namespace HealthcareERP.Modules.Hms.Contracts.Events;

public sealed record PatientChanged(Guid PatientId, string Mrn, string FullName, string Status);
