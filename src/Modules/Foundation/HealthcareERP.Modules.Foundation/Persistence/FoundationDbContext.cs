using HealthcareERP.BuildingBlocks.Infrastructure.Outbox;
using HealthcareERP.Modules.Foundation.Domain;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Foundation.Persistence;

public sealed class FoundationDbContext(DbContextOptions<FoundationDbContext> options) : DbContext(options)
{
    public DbSet<Facility> Facilities => Set<Facility>();
    public DbSet<OrgUnit> OrgUnits => Set<OrgUnit>();
    public DbSet<AppUser> Users => Set<AppUser>();
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

        modelBuilder.Entity<AppUser>(b =>
        {
            b.ToTable("users");
            b.HasKey(x => x.Id);
            b.HasIndex(x => x.UserName).IsUnique();
            b.Property(x => x.UserName).HasMaxLength(64).IsRequired();
            b.Property(x => x.DisplayName).HasMaxLength(200).IsRequired();
            b.Property(x => x.PasswordHash).HasMaxLength(128).IsRequired();
            b.Property(x => x.RolesCsv).HasMaxLength(256).IsRequired();
            b.Property(x => x.Status).HasMaxLength(32).IsRequired();
            b.Ignore(x => x.DomainEvents);
            b.Ignore(x => x.Roles);
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
