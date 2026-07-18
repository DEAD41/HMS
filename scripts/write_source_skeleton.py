#!/usr/bin/env python3
"""Write core modular-monolith source files."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def w(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    # remove default Class1.cs if writing nearby
    print("wrote", rel)


# Delete default Class1.cs files
for p in ROOT.rglob("Class1.cs"):
    p.unlink()
    print("removed", p)

w(
    "Directory.Build.props",
    """
<Project>
  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>false</TreatWarningsAsErrors>
    <LangVersion>latest</LangVersion>
  </PropertyGroup>
</Project>
""",
)

w(
    "src/BuildingBlocks/HealthcareERP.BuildingBlocks.Domain/Entity.cs",
    """
namespace HealthcareERP.BuildingBlocks.Domain;

public abstract class Entity
{
    public Guid Id { get; protected set; } = Guid.NewGuid();
    public DateTimeOffset CreatedAt { get; protected set; } = DateTimeOffset.UtcNow;
    public DateTimeOffset? UpdatedAt { get; protected set; }
    public byte[] RowVersion { get; protected set; } = Array.Empty<byte>();

    private readonly List<IDomainEvent> _domainEvents = [];
    public IReadOnlyCollection<IDomainEvent> DomainEvents => _domainEvents.AsReadOnly();

    protected void Raise(IDomainEvent domainEvent) => _domainEvents.Add(domainEvent);
    public void ClearDomainEvents() => _domainEvents.Clear();
    protected void Touch() => UpdatedAt = DateTimeOffset.UtcNow;
}
""",
)

w(
    "src/BuildingBlocks/HealthcareERP.BuildingBlocks.Domain/IDomainEvent.cs",
    """
namespace HealthcareERP.BuildingBlocks.Domain;

public interface IDomainEvent
{
    Guid EventId { get; }
    DateTimeOffset OccurredAt { get; }
    string EventType { get; }
}
""",
)

w(
    "src/BuildingBlocks/HealthcareERP.BuildingBlocks.Domain/DomainEvent.cs",
    """
namespace HealthcareERP.BuildingBlocks.Domain;

public abstract record DomainEvent : IDomainEvent
{
    public Guid EventId { get; init; } = Guid.NewGuid();
    public DateTimeOffset OccurredAt { get; init; } = DateTimeOffset.UtcNow;
    public abstract string EventType { get; }
}
""",
)

w(
    "src/BuildingBlocks/HealthcareERP.BuildingBlocks.Domain/AggregateRoot.cs",
    """
namespace HealthcareERP.BuildingBlocks.Domain;

public abstract class AggregateRoot : Entity;
""",
)

w(
    "src/BuildingBlocks/HealthcareERP.BuildingBlocks.Domain/Result.cs",
    """
namespace HealthcareERP.BuildingBlocks.Domain;

public class Result
{
    protected Result(bool isSuccess, string? error)
    {
        IsSuccess = isSuccess;
        Error = error;
    }

    public bool IsSuccess { get; }
    public bool IsFailure => !IsSuccess;
    public string? Error { get; }

    public static Result Success() => new(true, null);
    public static Result Failure(string error) => new(false, error);
    public static Result<T> Success<T>(T value) => Result<T>.Success(value);
    public static Result<T> Failure<T>(string error) => Result<T>.Failure(error);
}

public class Result<T> : Result
{
    private Result(T? value, bool isSuccess, string? error) : base(isSuccess, error) => Value = value;
    public T? Value { get; }
    public static Result<T> Success(T value) => new(value, true, null);
    public new static Result<T> Failure(string error) => new(default, false, error);
}
""",
)

w(
    "src/BuildingBlocks/HealthcareERP.BuildingBlocks.Contracts/IntegrationEvent.cs",
    """
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
""",
)

w(
    "src/BuildingBlocks/HealthcareERP.BuildingBlocks.Application/Abstractions/IIntegrationEventPublisher.cs",
    """
using HealthcareERP.BuildingBlocks.Contracts;

namespace HealthcareERP.BuildingBlocks.Application.Abstractions;

public interface IIntegrationEventPublisher
{
    Task EnqueueAsync(IntegrationEvent integrationEvent, CancellationToken cancellationToken = default);
}
""",
)

w(
    "src/BuildingBlocks/HealthcareERP.BuildingBlocks.Application/Abstractions/ICurrentUser.cs",
    """
namespace HealthcareERP.BuildingBlocks.Application.Abstractions;

public interface ICurrentUser
{
    Guid? UserId { get; }
    string? UserName { get; }
    Guid? FacilityId { get; }
    bool IsAuthenticated { get; }
}
""",
)

w(
    "src/BuildingBlocks/HealthcareERP.BuildingBlocks.Application/Abstractions/IAuditWriter.cs",
    """
namespace HealthcareERP.BuildingBlocks.Application.Abstractions;

public interface IAuditWriter
{
    Task WriteAsync(string module, string action, string entityType, Guid entityId, string? beforeJson, string? afterJson, CancellationToken cancellationToken = default);
}
""",
)

w(
    "src/BuildingBlocks/HealthcareERP.BuildingBlocks.Infrastructure/Outbox/OutboxMessage.cs",
    """
namespace HealthcareERP.BuildingBlocks.Infrastructure.Outbox;

public sealed class OutboxMessage
{
    public Guid Id { get; set; }
    public string EventType { get; set; } = string.Empty;
    public string Version { get; set; } = "v1";
    public DateTimeOffset OccurredAt { get; set; }
    public Guid? CorrelationId { get; set; }
    public Guid? CausationId { get; set; }
    public Guid FacilityId { get; set; }
    public string PartitionKey { get; set; } = string.Empty;
    public string PayloadJson { get; set; } = "{}";
    public string Status { get; set; } = "Pending";
    public int Attempts { get; set; }
    public string? LastError { get; set; }
    public DateTimeOffset? DispatchedAt { get; set; }
}
""",
)

w(
    "src/BuildingBlocks/HealthcareERP.BuildingBlocks.Infrastructure/Outbox/InboxMessage.cs",
    """
namespace HealthcareERP.BuildingBlocks.Infrastructure.Outbox;

public sealed class InboxMessage
{
    public Guid EventId { get; set; }
    public string EventType { get; set; } = string.Empty;
    public DateTimeOffset ReceivedAt { get; set; } = DateTimeOffset.UtcNow;
    public DateTimeOffset? ProcessedAt { get; set; }
    public string Status { get; set; } = "Received";
    public string? LastError { get; set; }
}
""",
)

w(
    "src/BuildingBlocks/HealthcareERP.BuildingBlocks.Infrastructure/Outbox/EfIntegrationEventPublisher.cs",
    """
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
        await Task.CompletedTask;
    }
}
""",
)

w(
    "src/BuildingBlocks/HealthcareERP.BuildingBlocks.Infrastructure/Outbox/IIntegrationEventHandler.cs",
    """
using HealthcareERP.BuildingBlocks.Contracts;

namespace HealthcareERP.BuildingBlocks.Infrastructure.Outbox;

public interface IIntegrationEventHandler
{
    string EventType { get; }
    Task HandleAsync(IntegrationEvent integrationEvent, CancellationToken cancellationToken = default);
}
""",
)

w(
    "src/BuildingBlocks/HealthcareERP.BuildingBlocks.Infrastructure/Outbox/OutboxDispatcher.cs",
    """
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

            inbox ??= new InboxMessage { EventId = message.Id, EventType = message.EventType };
            if (inbox.EventId == message.Id && inbox.Status != "Processed")
            {
                db.Set<InboxMessage>().Attach(inbox);
            }
            else if (await db.Set<InboxMessage>().FindAsync([message.Id], cancellationToken) is null)
            {
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
""",
)

# Foundation module
w(
    "src/Modules/Foundation/HealthcareERP.Modules.Foundation.Contracts/Events/FacilityCreated.cs",
    """
namespace HealthcareERP.Modules.Foundation.Contracts.Events;

public sealed record FacilityCreated(Guid FacilityId, string Code, string Name, string Timezone, string Currency);
""",
)

w(
    "src/Modules/Foundation/HealthcareERP.Modules.Foundation/Domain/Facility.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Foundation.Domain;

public sealed class Facility : AggregateRoot
{
    private Facility() { }

    public string Code { get; private set; } = string.Empty;
    public string Name { get; private set; } = string.Empty;
    public string Timezone { get; private set; } = "UTC";
    public string Currency { get; private set; } = "USD";
    public string Status { get; private set; } = "Draft";

    public static Result<Facility> Create(string code, string name, string timezone, string currency)
    {
        if (string.IsNullOrWhiteSpace(code)) return Result.Failure<Facility>("Facility code is required.");
        if (string.IsNullOrWhiteSpace(name)) return Result.Failure<Facility>("Facility name is required.");
        if (string.IsNullOrWhiteSpace(timezone)) return Result.Failure<Facility>("Timezone is required.");
        if (string.IsNullOrWhiteSpace(currency) || currency.Length != 3) return Result.Failure<Facility>("Currency must be ISO-4217.");

        var facility = new Facility
        {
            Code = code.Trim().ToUpperInvariant(),
            Name = name.Trim(),
            Timezone = timezone.Trim(),
            Currency = currency.Trim().ToUpperInvariant(),
            Status = "Active"
        };
        return Result.Success(facility);
    }

    public Result Activate()
    {
        Status = "Active";
        Touch();
        return Result.Success();
    }

    public Result Deactivate()
    {
        Status = "Inactive";
        Touch();
        return Result.Success();
    }
}
""",
)

w(
    "src/Modules/Foundation/HealthcareERP.Modules.Foundation/Domain/OrgUnit.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Foundation.Domain;

public sealed class OrgUnit : AggregateRoot
{
    private OrgUnit() { }

    public Guid FacilityId { get; private set; }
    public string Code { get; private set; } = string.Empty;
    public string Name { get; private set; } = string.Empty;
    public string Type { get; private set; } = "Department";
    public Guid? ParentId { get; private set; }
    public Guid? CostCenterRef { get; private set; }
    public string Status { get; private set; } = "Active";

    public static Result<OrgUnit> Create(Guid facilityId, string code, string name, string type, Guid? parentId = null, Guid? costCenterRef = null)
    {
        if (facilityId == Guid.Empty) return Result.Failure<OrgUnit>("Facility is required.");
        if (string.IsNullOrWhiteSpace(code)) return Result.Failure<OrgUnit>("Org unit code is required.");
        if (string.IsNullOrWhiteSpace(name)) return Result.Failure<OrgUnit>("Org unit name is required.");
        var allowed = new HashSet<string>(StringComparer.OrdinalIgnoreCase) { "Department", "Ward", "Clinic", "Store", "Theatre", "Other" };
        if (!allowed.Contains(type)) return Result.Failure<OrgUnit>("Invalid org unit type.");

        return Result.Success(new OrgUnit
        {
            FacilityId = facilityId,
            Code = code.Trim().ToUpperInvariant(),
            Name = name.Trim(),
            Type = type,
            ParentId = parentId,
            CostCenterRef = costCenterRef,
            Status = "Active"
        });
    }

    public Result Deactivate()
    {
        Status = "Inactive";
        Touch();
        return Result.Success();
    }
}
""",
)

w(
    "src/Modules/Foundation/HealthcareERP.Modules.Foundation/Domain/AuditEvent.cs",
    """
namespace HealthcareERP.Modules.Foundation.Domain;

public sealed class AuditEvent
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public DateTimeOffset Timestamp { get; set; } = DateTimeOffset.UtcNow;
    public Guid? ActorUserId { get; set; }
    public string? ActorUserName { get; set; }
    public Guid? FacilityId { get; set; }
    public string Module { get; set; } = string.Empty;
    public string Action { get; set; } = string.Empty;
    public string EntityType { get; set; } = string.Empty;
    public Guid EntityId { get; set; }
    public string? BeforeJson { get; set; }
    public string? AfterJson { get; set; }
    public Guid? CorrelationId { get; set; }
}
""",
)

w(
    "src/Modules/Foundation/HealthcareERP.Modules.Foundation/Persistence/FoundationDbContext.cs",
    """
using HealthcareERP.BuildingBlocks.Infrastructure.Outbox;
using HealthcareERP.Modules.Foundation.Domain;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Foundation.Persistence;

public sealed class FoundationDbContext(DbContextOptions<FoundationDbContext> options) : DbContext(options)
{
    public DbSet<Facility> Facilities => Set<Facility>();
    public DbSet<OrgUnit> OrgUnits => Set<OrgUnit>();
    public DbSet<AuditEvent> AuditEvents => Set<AuditEvent>();
    public DbSet<OutboxMessage> OutboxMessages => Set<OutboxMessage>();
    public DbSet<InboxMessage> InboxMessages => Set<InboxMessage>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.HasDefaultSchema("fnd");

        modelBuilder.Entity<Facility>(b =>
        {
            b.ToTable("facilities");
            b.HasKey(x => x.Id);
            b.Property(x => x.Code).HasMaxLength(32).IsRequired();
            b.HasIndex(x => x.Code).IsUnique();
            b.Property(x => x.Name).HasMaxLength(200).IsRequired();
            b.Property(x => x.Timezone).HasMaxLength(64).IsRequired();
            b.Property(x => x.Currency).HasMaxLength(3).IsRequired();
            b.Property(x => x.Status).HasMaxLength(32).IsRequired();
            b.Property(x => x.RowVersion).IsConcurrencyToken();
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<OrgUnit>(b =>
        {
            b.ToTable("org_units");
            b.HasKey(x => x.Id);
            b.Property(x => x.Code).HasMaxLength(32).IsRequired();
            b.Property(x => x.Name).HasMaxLength(200).IsRequired();
            b.Property(x => x.Type).HasMaxLength(32).IsRequired();
            b.Property(x => x.Status).HasMaxLength(32).IsRequired();
            b.HasIndex(x => new { x.FacilityId, x.Code }).IsUnique();
            b.Property(x => x.RowVersion).IsConcurrencyToken();
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<AuditEvent>(b =>
        {
            b.ToTable("audit_events");
            b.HasKey(x => x.Id);
            b.Property(x => x.Module).HasMaxLength(64);
            b.Property(x => x.Action).HasMaxLength(64);
            b.Property(x => x.EntityType).HasMaxLength(128);
        });

        modelBuilder.Entity<OutboxMessage>(b =>
        {
            b.ToTable("outbox_messages");
            b.HasKey(x => x.Id);
            b.HasIndex(x => x.Status);
        });

        modelBuilder.Entity<InboxMessage>(b =>
        {
            b.ToTable("inbox_messages");
            b.HasKey(x => x.EventId);
        });
    }
}
""",
)

w(
    "src/Modules/Foundation/HealthcareERP.Modules.Foundation/Services/AuditWriter.cs",
    """
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.Modules.Foundation.Domain;
using HealthcareERP.Modules.Foundation.Persistence;

namespace HealthcareERP.Modules.Foundation.Services;

public sealed class AuditWriter(FoundationDbContext db, ICurrentUser currentUser) : IAuditWriter
{
    public async Task WriteAsync(string module, string action, string entityType, Guid entityId, string? beforeJson, string? afterJson, CancellationToken cancellationToken = default)
    {
        db.AuditEvents.Add(new AuditEvent
        {
            Module = module,
            Action = action,
            EntityType = entityType,
            EntityId = entityId,
            BeforeJson = beforeJson,
            AfterJson = afterJson,
            ActorUserId = currentUser.UserId,
            ActorUserName = currentUser.UserName,
            FacilityId = currentUser.FacilityId
        });
        await Task.CompletedTask;
    }
}
""",
)

w(
    "src/Modules/Foundation/HealthcareERP.Modules.Foundation/Services/FacilityService.cs",
    """
using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Foundation.Contracts.Events;
using HealthcareERP.Modules.Foundation.Domain;
using HealthcareERP.Modules.Foundation.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Foundation.Services;

public sealed class FacilityService(
    FoundationDbContext db,
    IIntegrationEventPublisher publisher,
    IAuditWriter auditWriter)
{
    public async Task<Result<Facility>> CreateAsync(string code, string name, string timezone, string currency, CancellationToken cancellationToken = default)
    {
        if (await db.Facilities.AnyAsync(x => x.Code == code.Trim().ToUpperInvariant(), cancellationToken))
            return Result.Failure<Facility>("Facility code already exists.");

        var create = Facility.Create(code, name, timezone, currency);
        if (create.IsFailure) return create;

        var facility = create.Value!;
        db.Facilities.Add(facility);

        var payload = new FacilityCreated(facility.Id, facility.Code, facility.Name, facility.Timezone, facility.Currency);
        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(),
            "FacilityCreated",
            "v1",
            DateTimeOffset.UtcNow,
            null,
            null,
            facility.Id,
            facility.Id.ToString(),
            JsonSerializer.Serialize(payload)), cancellationToken);

        await auditWriter.WriteAsync("FND", "Create", nameof(Facility), facility.Id, null, JsonSerializer.Serialize(payload), cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(facility);
    }

    public Task<List<Facility>> ListAsync(CancellationToken cancellationToken = default) =>
        db.Facilities.AsNoTracking().OrderBy(x => x.Code).ToListAsync(cancellationToken);

    public async Task<Result<OrgUnit>> CreateOrgUnitAsync(Guid facilityId, string code, string name, string type, Guid? parentId, Guid? costCenterRef, CancellationToken cancellationToken = default)
    {
        var facility = await db.Facilities.FirstOrDefaultAsync(x => x.Id == facilityId, cancellationToken);
        if (facility is null) return Result.Failure<OrgUnit>("Facility not found.");
        if (!string.Equals(facility.Status, "Active", StringComparison.OrdinalIgnoreCase))
            return Result.Failure<OrgUnit>("Facility is not active.");

        if (await db.OrgUnits.AnyAsync(x => x.FacilityId == facilityId && x.Code == code.Trim().ToUpperInvariant(), cancellationToken))
            return Result.Failure<OrgUnit>("Org unit code already exists in facility.");

        var create = OrgUnit.Create(facilityId, code, name, type, parentId, costCenterRef);
        if (create.IsFailure) return create;

        db.OrgUnits.Add(create.Value!);
        await auditWriter.WriteAsync("FND", "Create", nameof(OrgUnit), create.Value!.Id, null, JsonSerializer.Serialize(new { create.Value.Code, create.Value.Name, create.Value.Type }), cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public Task<List<OrgUnit>> ListOrgUnitsAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.OrgUnits.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderBy(x => x.Code).ToListAsync(cancellationToken);
}
""",
)

w(
    "src/Modules/Foundation/HealthcareERP.Modules.Foundation/DependencyInjection.cs",
    """
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Infrastructure.Outbox;
using HealthcareERP.Modules.Foundation.Persistence;
using HealthcareERP.Modules.Foundation.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace HealthcareERP.Modules.Foundation;

public static class DependencyInjection
{
    public static IServiceCollection AddFoundationModule(this IServiceCollection services, string? connectionString, bool useInMemory = false)
    {
        if (useInMemory || string.IsNullOrWhiteSpace(connectionString))
        {
            services.AddDbContext<FoundationDbContext>(o => o.UseInMemoryDatabase("healthcare-erp"));
        }
        else
        {
            services.AddDbContext<FoundationDbContext>(o => o.UseNpgsql(connectionString));
        }

        services.AddScoped<IIntegrationEventPublisher, EfIntegrationEventPublisher<FoundationDbContext>>();
        services.AddScoped<IAuditWriter, AuditWriter>();
        services.AddScoped<FacilityService>();
        services.AddHostedService<OutboxDispatcher<FoundationDbContext>>();
        return services;
    }
}
""",
)

print("foundation core done")
print("OK")
