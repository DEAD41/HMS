namespace HealthcareERP.Modules.Financials.Contracts.Events;

public sealed record JournalPosted(Guid JournalId, Guid FacilityId, string SourceDocumentId, decimal TotalDebit);
