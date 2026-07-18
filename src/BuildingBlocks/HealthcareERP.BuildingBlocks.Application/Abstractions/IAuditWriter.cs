namespace HealthcareERP.BuildingBlocks.Application.Abstractions;

public interface IAuditWriter
{
    Task WriteAsync(string module, string action, string entityType, Guid entityId, string? beforeJson, string? afterJson, CancellationToken cancellationToken = default);
}
