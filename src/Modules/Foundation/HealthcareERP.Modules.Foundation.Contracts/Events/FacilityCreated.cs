namespace HealthcareERP.Modules.Foundation.Contracts.Events;

public sealed record FacilityCreated(Guid FacilityId, string Code, string Name, string Timezone, string Currency);
