using HealthcareERP.Modules.Financials.Domain;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Financials.Persistence;

public sealed class FinancialsDbContext(DbContextOptions<FinancialsDbContext> options) : DbContext(options)
{
    public DbSet<Account> Accounts => Set<Account>();
    public DbSet<CostCenter> CostCenters => Set<CostCenter>();
    public DbSet<Receivable> Receivables => Set<Receivable>();
    public DbSet<VendorInvoice> VendorInvoices => Set<VendorInvoice>();
    public DbSet<PayrollExpense> PayrollExpenses => Set<PayrollExpense>();
    public DbSet<BudgetLine> BudgetLines => Set<BudgetLine>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.HasDefaultSchema("fin");

        modelBuilder.Entity<Account>(b =>
        {
            b.ToTable("accounts");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.FacilityId, x.Code }).IsUnique();
            b.Property(x => x.Code).HasMaxLength(32);
            b.Property(x => x.Name).HasMaxLength(200);
            b.Property(x => x.Type).HasMaxLength(32);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<CostCenter>(b =>
        {
            b.ToTable("cost_centers");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.FacilityId, x.Code }).IsUnique();
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<Receivable>(b =>
        {
            b.ToTable("receivables");
            b.HasKey(x => x.Id);
            b.HasIndex(x => x.SourceChargeId).IsUnique();
            b.Property(x => x.Amount).HasPrecision(18, 2);
            b.Property(x => x.SettledAmount).HasPrecision(18, 2);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<VendorInvoice>(b =>
        {
            b.ToTable("vendor_invoices");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.VendorId, x.InvoiceNumber }).IsUnique();
            b.Property(x => x.Amount).HasPrecision(18, 2);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<PayrollExpense>(b =>
        {
            b.ToTable("payroll_expenses");
            b.HasKey(x => x.Id);
            b.HasIndex(x => x.PayrollRunId).IsUnique();
            b.Property(x => x.GrossAmount).HasPrecision(18, 2);
            b.Property(x => x.NetAmount).HasPrecision(18, 2);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<BudgetLine>(b =>
        {
            b.ToTable("budget_lines");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.FacilityId, x.CostCenterId, x.Period, x.AccountCode });
            b.Property(x => x.Amount).HasPrecision(18, 2);
            b.Property(x => x.ActualAmount).HasPrecision(18, 2);
            b.Ignore(x => x.DomainEvents);
            b.Ignore(x => x.Variance);
            b.Ignore(x => x.UtilizationPercent);
        });
    }
}
