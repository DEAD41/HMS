using HealthcareERP.Modules.Hms.Domain;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Persistence;

public sealed class HmsDbContext(DbContextOptions<HmsDbContext> options) : DbContext(options)
{
    public DbSet<Patient> Patients => Set<Patient>();
    public DbSet<Appointment> Appointments => Set<Appointment>();
    public DbSet<OpdEncounter> OpdEncounters => Set<OpdEncounter>();
    public DbSet<Charge> Charges => Set<Charge>();
    public DbSet<Bed> Beds => Set<Bed>();
    public DbSet<Admission> Admissions => Set<Admission>();
    public DbSet<ErEncounter> ErEncounters => Set<ErEncounter>();
    public DbSet<OtCase> OtCases => Set<OtCase>();
    public DbSet<LabOrder> LabOrders => Set<LabOrder>();
    public DbSet<RadiologyOrder> RadiologyOrders => Set<RadiologyOrder>();
    public DbSet<MedicationDispense> MedicationDispenses => Set<MedicationDispense>();
    public DbSet<DischargeProcess> DischargeProcesses => Set<DischargeProcess>();
    public DbSet<NursingCarePlan> NursingCarePlans => Set<NursingCarePlan>();
    public DbSet<MarEntry> MarEntries => Set<MarEntry>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.HasDefaultSchema("hms");

        modelBuilder.Entity<Patient>(b =>
        {
            b.ToTable("patients");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.FacilityId, x.Mrn }).IsUnique();
            b.Property(x => x.Mrn).HasMaxLength(32);
            b.Property(x => x.FirstName).HasMaxLength(100);
            b.Property(x => x.LastName).HasMaxLength(100);
            b.Property(x => x.Status).HasMaxLength(32);
            b.Ignore(x => x.DomainEvents);
            b.Ignore(x => x.FullName);
        });

        modelBuilder.Entity<Appointment>(b =>
        {
            b.ToTable("appointments");
            b.HasKey(x => x.Id);
            b.Property(x => x.Status).HasMaxLength(32);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<OpdEncounter>(b =>
        {
            b.ToTable("opd_encounters");
            b.HasKey(x => x.Id);
            b.Property(x => x.Status).HasMaxLength(32);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<Charge>(b =>
        {
            b.ToTable("charges");
            b.HasKey(x => x.Id);
            b.Property(x => x.Amount).HasPrecision(18, 2);
            b.Property(x => x.ChargeCode).HasMaxLength(32);
            b.Property(x => x.Currency).HasMaxLength(3);
            b.HasIndex(x => x.SourceEventId);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<Bed>(b =>
        {
            b.ToTable("beds");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.FacilityId, x.Code }).IsUnique();
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<Admission>(b =>
        {
            b.ToTable("admissions");
            b.HasKey(x => x.Id);
            b.Property(x => x.Status).HasMaxLength(32);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<ErEncounter>(b =>
        {
            b.ToTable("er_encounters");
            b.HasKey(x => x.Id);
            b.Property(x => x.Status).HasMaxLength(32);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<OtCase>(b =>
        {
            b.ToTable("ot_cases");
            b.HasKey(x => x.Id);
            b.Property(x => x.Status).HasMaxLength(32);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<LabOrder>(b =>
        {
            b.ToTable("lab_orders");
            b.HasKey(x => x.Id);
            b.Property(x => x.Status).HasMaxLength(32);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<RadiologyOrder>(b =>
        {
            b.ToTable("radiology_orders");
            b.HasKey(x => x.Id);
            b.Property(x => x.Status).HasMaxLength(32);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<MedicationDispense>(b =>
        {
            b.ToTable("medication_dispenses");
            b.HasKey(x => x.Id);
            b.Property(x => x.Quantity).HasPrecision(18, 2);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<DischargeProcess>(b =>
        {
            b.ToTable("discharge_processes");
            b.HasKey(x => x.Id);
            b.Property(x => x.Status).HasMaxLength(32);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<NursingCarePlan>(b =>
        {
            b.ToTable("nursing_care_plans");
            b.HasKey(x => x.Id);
            b.HasIndex(x => x.AdmissionId);
            b.Property(x => x.Status).HasMaxLength(32);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<MarEntry>(b =>
        {
            b.ToTable("mar_entries");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.AdmissionId, x.DoseInstanceId }).IsUnique();
            b.Property(x => x.DoseInstanceId).HasMaxLength(64);
            b.Property(x => x.Status).HasMaxLength(32);
            b.Ignore(x => x.DomainEvents);
        });
    }
}
