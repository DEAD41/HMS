namespace HealthcareERP.Modules.Hris.Contracts.Events;

public sealed record PayrollPosted(Guid PayrollRunId, Guid FacilityId, string Period, decimal GrossAmount, decimal NetAmount);
