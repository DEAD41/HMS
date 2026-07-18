using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.BuildingBlocks.Infrastructure.Outbox;

public sealed class EfIntegrationEventPublisher<TDbContext>(TDbContext dbContext) : IIntegrationEventPublisher
    where TDbContext : DbContext
{
    public async Task EnqueueAsync(IntegrationEvent integrationEvent, CancellationToken cancellationToken = default)
    {
        dbContext.Set<OutboxMessage>().Add(new OutboxMessage
        {
            Id = integrationEvent.EventId,
            EventType = integrationEvent.EventType,
            Version = integrationEvent.Version,
            OccurredAt = integrationEvent.OccurredAt,
            CorrelationId = integrationEvent.CorrelationId,
            CausationId = integrationEvent.CausationId,
            FacilityId = integrationEvent.FacilityId,
            PartitionKey = integrationEvent.PartitionKey,
            PayloadJson = integrationEvent.PayloadJson,
            Status = "Pending"
        });

        // MVP: persist outbox immediately. Later increments will enlist business + outbox in one transaction.
        await dbContext.SaveChangesAsync(cancellationToken);
    }
}
