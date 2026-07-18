using HealthcareERP.Modules.Inventory.Domain;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Inventory.Persistence;

public sealed class InventoryDbContext(DbContextOptions<InventoryDbContext> options) : DbContext(options)
{
    public DbSet<Item> Items => Set<Item>();
    public DbSet<Store> Stores => Set<Store>();
    public DbSet<StockBalance> StockBalances => Set<StockBalance>();
    public DbSet<Batch> Batches => Set<Batch>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.HasDefaultSchema("inv");

        modelBuilder.Entity<Item>(b =>
        {
            b.ToTable("items");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.FacilityId, x.Sku }).IsUnique();
            b.Property(x => x.ReorderLevel).HasPrecision(18, 2);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<Store>(b =>
        {
            b.ToTable("stores");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.FacilityId, x.Code }).IsUnique();
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<StockBalance>(b =>
        {
            b.ToTable("stock_balances");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.StoreId, x.ItemId }).IsUnique();
            b.Property(x => x.QuantityOnHand).HasPrecision(18, 2);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<Batch>(b =>
        {
            b.ToTable("batches");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.FacilityId, x.StoreId, x.ItemId, x.BatchNumber }).IsUnique();
            b.Property(x => x.BatchNumber).HasMaxLength(64);
            b.Property(x => x.QuantityOnHand).HasPrecision(18, 2);
            b.Property(x => x.Status).HasMaxLength(32);
            b.Ignore(x => x.DomainEvents);
        });
    }
}
