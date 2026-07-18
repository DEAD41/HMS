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

        // MVP: persist audit immediately so module DbContexts remain independent.
        await db.SaveChangesAsync(cancellationToken);
    }
}
