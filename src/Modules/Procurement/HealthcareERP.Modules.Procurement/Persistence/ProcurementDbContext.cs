using HealthcareERP.Modules.Procurement.Domain;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Procurement.Persistence;

public sealed class ProcurementDbContext(DbContextOptions<ProcurementDbContext> options) : DbContext(options)
{
    public DbSet<Vendor> Vendors => Set<Vendor>();
    public DbSet<PurchaseRequisition> PurchaseRequisitions => Set<PurchaseRequisition>();
    public DbSet<PurchaseOrder> PurchaseOrders => Set<PurchaseOrder>();
    public DbSet<VendorScorecard> VendorScorecards => Set<VendorScorecard>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.HasDefaultSchema("prc");

        modelBuilder.Entity<Vendor>(b =>
        {
            b.ToTable("vendors");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.FacilityId, x.Code }).IsUnique();
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<PurchaseRequisition>(b =>
        {
            b.ToTable("purchase_requisitions");
            b.HasKey(x => x.Id);
            b.HasIndex(x => x.SignalId);
            b.Property(x => x.Quantity).HasPrecision(18, 2);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<PurchaseOrder>(b =>
        {
            b.ToTable("purchase_orders");
            b.HasKey(x => x.Id);
            b.Property(x => x.Quantity).HasPrecision(18, 2);
            b.Property(x => x.UnitPrice).HasPrecision(18, 2);
            b.Ignore(x => x.DomainEvents);
            b.Ignore(x => x.TotalAmount);
        });

        modelBuilder.Entity<VendorScorecard>(b =>
        {
            b.ToTable("vendor_scorecards");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.FacilityId, x.VendorId, x.Period }).IsUnique();
            b.Property(x => x.TotalSpend).HasPrecision(18, 2);
            b.Property(x => x.OnTimePercent).HasPrecision(18, 2);
            b.Property(x => x.QualityPercent).HasPrecision(18, 2);
            b.Property(x => x.OverallScore).HasPrecision(18, 2);
            b.Ignore(x => x.DomainEvents);
        });
    }
}
