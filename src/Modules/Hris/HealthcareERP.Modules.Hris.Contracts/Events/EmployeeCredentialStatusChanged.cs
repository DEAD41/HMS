namespace HealthcareERP.Modules.Hris.Contracts.Events;

public sealed record EmployeeCredentialStatusChanged(Guid EmployeeId, Guid FacilityId, string Status, bool IsSchedulable);
