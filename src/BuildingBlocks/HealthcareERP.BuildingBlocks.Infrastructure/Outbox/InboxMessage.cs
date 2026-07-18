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
