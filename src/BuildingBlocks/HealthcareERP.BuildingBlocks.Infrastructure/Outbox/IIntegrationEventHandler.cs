using HealthcareERP.BuildingBlocks.Contracts;

namespace HealthcareERP.BuildingBlocks.Infrastructure.Outbox;

public interface IIntegrationEventHandler
{
    string EventType { get; }
    Task HandleAsync(IntegrationEvent integrationEvent, CancellationToken cancellationToken = default);
}
