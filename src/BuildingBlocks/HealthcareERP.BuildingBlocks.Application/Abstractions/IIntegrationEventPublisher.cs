using HealthcareERP.BuildingBlocks.Contracts;

namespace HealthcareERP.BuildingBlocks.Application.Abstractions;

public interface IIntegrationEventPublisher
{
    Task EnqueueAsync(IntegrationEvent integrationEvent, CancellationToken cancellationToken = default);
}
