namespace HealthcareERP.Modules.Hris.Contracts.Events;

public sealed record EmployeeChanged(Guid EmployeeId, string EmployeeCode, string FullName, string Status);
