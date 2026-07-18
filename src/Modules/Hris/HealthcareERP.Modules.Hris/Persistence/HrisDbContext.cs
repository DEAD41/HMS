using HealthcareERP.Modules.Hris.Domain;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hris.Persistence;

public sealed class HrisDbContext(DbContextOptions<HrisDbContext> options) : DbContext(options)
{
    public DbSet<Employee> Employees => Set<Employee>();
    public DbSet<Credential> Credentials => Set<Credential>();
    public DbSet<RosterAssignment> RosterAssignments => Set<RosterAssignment>();
    public DbSet<LeaveRequest> LeaveRequests => Set<LeaveRequest>();
    public DbSet<PayrollRun> PayrollRuns => Set<PayrollRun>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.HasDefaultSchema("hris");

        modelBuilder.Entity<Employee>(b =>
        {
            b.ToTable("employees");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.FacilityId, x.EmployeeCode }).IsUnique();
            b.Ignore(x => x.DomainEvents);
            b.Ignore(x => x.FullName);
        });

        modelBuilder.Entity<Credential>(b =>
        {
            b.ToTable("credentials");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.EmployeeId, x.Type, x.Number });
            b.Ignore(x => x.DomainEvents);
            b.Ignore(x => x.IsSchedulable);
        });

        modelBuilder.Entity<RosterAssignment>(b =>
        {
            b.ToTable("roster_assignments");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.EmployeeId, x.DutyDate, x.ShiftCode }).IsUnique();
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<LeaveRequest>(b =>
        {
            b.ToTable("leave_requests");
            b.HasKey(x => x.Id);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<PayrollRun>(b =>
        {
            b.ToTable("payroll_runs");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.FacilityId, x.Period }).IsUnique();
            b.Property(x => x.GrossAmount).HasPrecision(18, 2);
            b.Property(x => x.Deductions).HasPrecision(18, 2);
            b.Property(x => x.NetAmount).HasPrecision(18, 2);
            b.Ignore(x => x.DomainEvents);
        });
    }
}
