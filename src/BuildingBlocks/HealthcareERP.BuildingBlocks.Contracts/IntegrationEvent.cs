namespace HealthcareERP.BuildingBlocks.Contracts;

public sealed record IntegrationEvent(
    Guid EventId,
    string EventType,
    string Version,
    DateTimeOffset OccurredAt,
    Guid? CorrelationId,
    Guid? CausationId,
    Guid FacilityId,
    string PartitionKey,
    string PayloadJson);
