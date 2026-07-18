using System.Text.Json;
using HealthcareERP.BuildingBlocks.Contracts;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace HealthcareERP.BuildingBlocks.Infrastructure.Outbox;

public sealed class OutboxDispatcher<TDbContext>(
    IServiceScopeFactory scopeFactory,
    ILogger<OutboxDispatcher<TDbContext>> logger) : BackgroundService
    where TDbContext : DbContext
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await DispatchBatchAsync(stoppingToken);
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "Outbox dispatch loop failed");
            }

            await Task.Delay(TimeSpan.FromSeconds(2), stoppingToken);
        }
    }

    private async Task DispatchBatchAsync(CancellationToken cancellationToken)
    {
        using var scope = scopeFactory.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<TDbContext>();
        var handlers = scope.ServiceProvider.GetServices<IIntegrationEventHandler>().ToList();

        var messages = await db.Set<OutboxMessage>()
            .Where(x => x.Status == "Pending" || x.Status == "Failed")
            .OrderBy(x => x.OccurredAt)
            .Take(50)
            .ToListAsync(cancellationToken);

        foreach (var message in messages)
        {
            var integrationEvent = new IntegrationEvent(
                message.Id,
                message.EventType,
                message.Version,
                message.OccurredAt,
                message.CorrelationId,
                message.CausationId,
                message.FacilityId,
                message.PartitionKey,
                message.PayloadJson);

            var inbox = await db.Set<InboxMessage>().FindAsync([message.Id], cancellationToken);
            if (inbox is { Status: "Processed" })
            {
                message.Status = "Completed";
                message.DispatchedAt = DateTimeOffset.UtcNow;
                continue;
            }

            if (inbox is null)
            {
                inbox = new InboxMessage { EventId = message.Id, EventType = message.EventType };
                db.Set<InboxMessage>().Add(inbox);
            }

            try
            {
                foreach (var handler in handlers.Where(h => h.EventType == message.EventType))
                {
                    await handler.HandleAsync(integrationEvent, cancellationToken);
                }

                inbox.Status = "Processed";
                inbox.ProcessedAt = DateTimeOffset.UtcNow;
                message.Status = "Completed";
                message.DispatchedAt = DateTimeOffset.UtcNow;
                message.LastError = null;
            }
            catch (Exception ex)
            {
                message.Attempts += 1;
                message.Status = message.Attempts >= 5 ? "DeadLetter" : "Failed";
                message.LastError = ex.Message;
                inbox.Status = "DeadLetter";
                inbox.LastError = ex.Message;
                logger.LogError(ex, "Failed handling outbox message {EventId} {EventType}", message.Id, message.EventType);
            }
        }

        if (messages.Count > 0)
        {
            await db.SaveChangesAsync(cancellationToken);
        }
    }
}
