#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def w(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print("wrote", rel)


# HMS
w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms.Contracts/Events/PatientChanged.cs",
    """
namespace HealthcareERP.Modules.Hms.Contracts.Events;

public sealed record PatientChanged(Guid PatientId, string Mrn, string FullName, string Status);
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Domain/Patient.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class Patient : AggregateRoot
{
    private Patient() { }

    public Guid FacilityId { get; private set; }
    public string Mrn { get; private set; } = string.Empty;
    public string FirstName { get; private set; } = string.Empty;
    public string LastName { get; private set; } = string.Empty;
    public DateOnly? DateOfBirth { get; private set; }
    public string? Phone { get; private set; }
    public string? NationalId { get; private set; }
    public string Status { get; private set; } = "Active";

    public string FullName => $"{FirstName} {LastName}".Trim();

    public static Result<Patient> Register(
        Guid facilityId,
        string mrn,
        string firstName,
        string lastName,
        DateOnly? dateOfBirth,
        string? phone,
        string? nationalId)
    {
        if (facilityId == Guid.Empty) return Result.Failure<Patient>("Facility is required.");
        if (string.IsNullOrWhiteSpace(mrn)) return Result.Failure<Patient>("MRN is required.");
        if (string.IsNullOrWhiteSpace(firstName)) return Result.Failure<Patient>("First name is required.");
        if (string.IsNullOrWhiteSpace(lastName)) return Result.Failure<Patient>("Last name is required.");

        return Result.Success(new Patient
        {
            FacilityId = facilityId,
            Mrn = mrn.Trim().ToUpperInvariant(),
            FirstName = firstName.Trim(),
            LastName = lastName.Trim(),
            DateOfBirth = dateOfBirth,
            Phone = phone?.Trim(),
            NationalId = nationalId?.Trim(),
            Status = "Active"
        });
    }
}
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Domain/Appointment.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class Appointment : AggregateRoot
{
    private Appointment() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid ClinicianEmployeeId { get; private set; }
    public Guid? ClinicOrgUnitId { get; private set; }
    public DateTimeOffset StartsAt { get; private set; }
    public DateTimeOffset EndsAt { get; private set; }
    public string Status { get; private set; } = "Scheduled";
    public string? Reason { get; private set; }

    public static Result<Appointment> Schedule(
        Guid facilityId,
        Guid patientId,
        Guid clinicianEmployeeId,
        DateTimeOffset startsAt,
        DateTimeOffset endsAt,
        Guid? clinicOrgUnitId,
        string? reason)
    {
        if (endsAt <= startsAt) return Result.Failure<Appointment>("Appointment end must be after start.");
        if (patientId == Guid.Empty || clinicianEmployeeId == Guid.Empty)
            return Result.Failure<Appointment>("Patient and clinician are required.");

        return Result.Success(new Appointment
        {
            FacilityId = facilityId,
            PatientId = patientId,
            ClinicianEmployeeId = clinicianEmployeeId,
            ClinicOrgUnitId = clinicOrgUnitId,
            StartsAt = startsAt,
            EndsAt = endsAt,
            Reason = reason,
            Status = "Scheduled"
        });
    }

    public Result CheckIn()
    {
        if (Status is not ("Scheduled")) return Result.Failure("Only scheduled appointments can be checked in.");
        Status = "CheckedIn";
        Touch();
        return Result.Success();
    }
}
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Domain/OpdEncounter.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class OpdEncounter : AggregateRoot
{
    private OpdEncounter() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid? AppointmentId { get; private set; }
    public Guid ClinicianEmployeeId { get; private set; }
    public string Status { get; private set; } = "Open";
    public string? ChiefComplaint { get; private set; }
    public string? Disposition { get; private set; }

    public static Result<OpdEncounter> Open(Guid facilityId, Guid patientId, Guid clinicianEmployeeId, Guid? appointmentId, string? chiefComplaint)
    {
        return Result.Success(new OpdEncounter
        {
            FacilityId = facilityId,
            PatientId = patientId,
            ClinicianEmployeeId = clinicianEmployeeId,
            AppointmentId = appointmentId,
            ChiefComplaint = chiefComplaint,
            Status = "Open"
        });
    }

    public Result Close(string disposition)
    {
        if (Status == "Closed") return Result.Failure("Encounter already closed.");
        if (string.IsNullOrWhiteSpace(disposition)) return Result.Failure("Disposition is required.");
        Status = "Closed";
        Disposition = disposition.Trim();
        Touch();
        return Result.Success();
    }
}
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Domain/Charge.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class Charge : AggregateRoot
{
    private Charge() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid? EncounterId { get; private set; }
    public string ChargeCode { get; private set; } = string.Empty;
    public string Description { get; private set; } = string.Empty;
    public decimal Amount { get; private set; }
    public string Currency { get; private set; } = "USD";
    public Guid? SourceEventId { get; private set; }
    public string Status { get; private set; } = "Open";

    public static Result<Charge> Create(
        Guid facilityId,
        Guid patientId,
        string chargeCode,
        string description,
        decimal amount,
        string currency,
        Guid? encounterId,
        Guid? sourceEventId)
    {
        if (amount < 0) return Result.Failure<Charge>("Amount cannot be negative.");
        if (string.IsNullOrWhiteSpace(chargeCode)) return Result.Failure<Charge>("Charge code is required.");

        return Result.Success(new Charge
        {
            FacilityId = facilityId,
            PatientId = patientId,
            EncounterId = encounterId,
            ChargeCode = chargeCode.Trim().ToUpperInvariant(),
            Description = description.Trim(),
            Amount = amount,
            Currency = currency.Trim().ToUpperInvariant(),
            SourceEventId = sourceEventId,
            Status = "Open"
        });
    }
}
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Persistence/HmsDbContext.cs",
    """
using HealthcareERP.Modules.Hms.Domain;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Persistence;

public sealed class HmsDbContext(DbContextOptions<HmsDbContext> options) : DbContext(options)
{
    public DbSet<Patient> Patients => Set<Patient>();
    public DbSet<Appointment> Appointments => Set<Appointment>();
    public DbSet<OpdEncounter> OpdEncounters => Set<OpdEncounter>();
    public DbSet<Charge> Charges => Set<Charge>();

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
            b.HasIndex(x => x.SourceEventId).IsUnique().HasFilter("\"SourceEventId\" IS NOT NULL");
            b.Ignore(x => x.DomainEvents);
        });
    }
}
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Services/PatientService.cs",
    """
using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Contracts.Events;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class PatientService(HmsDbContext db, IIntegrationEventPublisher publisher, IAuditWriter auditWriter)
{
    public async Task<Result<Patient>> RegisterAsync(
        Guid facilityId,
        string mrn,
        string firstName,
        string lastName,
        DateOnly? dateOfBirth,
        string? phone,
        string? nationalId,
        CancellationToken cancellationToken = default)
    {
        if (await db.Patients.AnyAsync(x => x.FacilityId == facilityId && x.Mrn == mrn.Trim().ToUpperInvariant(), cancellationToken))
            return Result.Failure<Patient>("MRN already exists for facility.");

        var create = Patient.Register(facilityId, mrn, firstName, lastName, dateOfBirth, phone, nationalId);
        if (create.IsFailure) return create;

        var patient = create.Value!;
        db.Patients.Add(patient);

        var payload = new PatientChanged(patient.Id, patient.Mrn, patient.FullName, patient.Status);
        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(), "PatientChanged", "v1", DateTimeOffset.UtcNow, null, null, facilityId, patient.Id.ToString(),
            JsonSerializer.Serialize(payload)), cancellationToken);

        await auditWriter.WriteAsync("HMS", "Register", nameof(Patient), patient.Id, null, JsonSerializer.Serialize(payload), cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(patient);
    }

    public Task<List<Patient>> SearchAsync(Guid facilityId, string? query, CancellationToken cancellationToken = default)
    {
        var q = db.Patients.AsNoTracking().Where(x => x.FacilityId == facilityId);
        if (!string.IsNullOrWhiteSpace(query))
        {
            var term = query.Trim().ToUpperInvariant();
            q = q.Where(x => x.Mrn.Contains(term) || x.FirstName.ToUpper().Contains(term) || x.LastName.ToUpper().Contains(term));
        }
        return q.OrderBy(x => x.Mrn).Take(50).ToListAsync(cancellationToken);
    }
}
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Services/AppointmentService.cs",
    """
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class AppointmentService(HmsDbContext db, IAuditWriter auditWriter)
{
    public async Task<Result<Appointment>> ScheduleAsync(
        Guid facilityId,
        Guid patientId,
        Guid clinicianEmployeeId,
        DateTimeOffset startsAt,
        DateTimeOffset endsAt,
        Guid? clinicOrgUnitId,
        string? reason,
        CancellationToken cancellationToken = default)
    {
        if (!await db.Patients.AnyAsync(x => x.Id == patientId && x.FacilityId == facilityId, cancellationToken))
            return Result.Failure<Appointment>("Patient not found.");

        var overlap = await db.Appointments.AnyAsync(x =>
            x.ClinicianEmployeeId == clinicianEmployeeId &&
            x.Status != "Cancelled" &&
            x.StartsAt < endsAt &&
            startsAt < x.EndsAt, cancellationToken);
        if (overlap) return Result.Failure<Appointment>("Clinician has a conflicting appointment.");

        var create = Appointment.Schedule(facilityId, patientId, clinicianEmployeeId, startsAt, endsAt, clinicOrgUnitId, reason);
        if (create.IsFailure) return create;

        db.Appointments.Add(create.Value!);
        await auditWriter.WriteAsync("HMS", "Schedule", nameof(Appointment), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<Appointment>> CheckInAsync(Guid appointmentId, CancellationToken cancellationToken = default)
    {
        var appointment = await db.Appointments.FirstOrDefaultAsync(x => x.Id == appointmentId, cancellationToken);
        if (appointment is null) return Result.Failure<Appointment>("Appointment not found.");
        var result = appointment.CheckIn();
        if (result.IsFailure) return Result.Failure<Appointment>(result.Error!);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(appointment);
    }

    public Task<List<Appointment>> ListAsync(Guid facilityId, DateOnly date, CancellationToken cancellationToken = default)
    {
        var start = date.ToDateTime(TimeOnly.MinValue, DateTimeKind.Utc);
        var end = date.ToDateTime(TimeOnly.MaxValue, DateTimeKind.Utc);
        return db.Appointments.AsNoTracking()
            .Where(x => x.FacilityId == facilityId && x.StartsAt >= start && x.StartsAt <= end)
            .OrderBy(x => x.StartsAt)
            .ToListAsync(cancellationToken);
    }
}
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Services/OpdService.cs",
    """
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class OpdService(HmsDbContext db, BillingService billingService, IAuditWriter auditWriter)
{
    public async Task<Result<OpdEncounter>> OpenAsync(
        Guid facilityId,
        Guid patientId,
        Guid clinicianEmployeeId,
        Guid? appointmentId,
        string? chiefComplaint,
        CancellationToken cancellationToken = default)
    {
        if (!await db.Patients.AnyAsync(x => x.Id == patientId, cancellationToken))
            return Result.Failure<OpdEncounter>("Patient not found.");

        if (appointmentId is Guid apptId)
        {
            var appt = await db.Appointments.FirstOrDefaultAsync(x => x.Id == apptId, cancellationToken);
            if (appt is null) return Result.Failure<OpdEncounter>("Appointment not found.");
            if (appt.Status != "CheckedIn" && appt.Status != "InProgress")
                return Result.Failure<OpdEncounter>("Appointment must be checked in.");
        }

        var create = OpdEncounter.Open(facilityId, patientId, clinicianEmployeeId, appointmentId, chiefComplaint);
        db.OpdEncounters.Add(create.Value!);
        await auditWriter.WriteAsync("HMS", "Open", nameof(OpdEncounter), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<OpdEncounter>> CloseAsync(Guid encounterId, string disposition, decimal consultationFee, string currency, CancellationToken cancellationToken = default)
    {
        var encounter = await db.OpdEncounters.FirstOrDefaultAsync(x => x.Id == encounterId, cancellationToken);
        if (encounter is null) return Result.Failure<OpdEncounter>("Encounter not found.");

        var close = encounter.Close(disposition);
        if (close.IsFailure) return Result.Failure<OpdEncounter>(close.Error!);

        if (consultationFee > 0)
        {
            var charge = await billingService.PostChargeAsync(
                encounter.FacilityId,
                encounter.PatientId,
                "OPDCONSULT",
                "OPD Consultation",
                consultationFee,
                currency,
                encounter.Id,
                Guid.NewGuid(),
                cancellationToken);
            if (charge.IsFailure) return Result.Failure<OpdEncounter>(charge.Error!);
        }

        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(encounter);
    }
}
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/Services/BillingService.cs",
    """
using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hms.Domain;
using HealthcareERP.Modules.Hms.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hms.Services;

public sealed class BillingService(HmsDbContext db, IIntegrationEventPublisher publisher, IAuditWriter auditWriter)
{
    public async Task<Result<Charge>> PostChargeAsync(
        Guid facilityId,
        Guid patientId,
        string chargeCode,
        string description,
        decimal amount,
        string currency,
        Guid? encounterId,
        Guid? sourceEventId,
        CancellationToken cancellationToken = default)
    {
        if (sourceEventId is Guid sid && await db.Charges.AnyAsync(x => x.SourceEventId == sid, cancellationToken))
        {
            var existing = await db.Charges.FirstAsync(x => x.SourceEventId == sid, cancellationToken);
            return Result.Success(existing);
        }

        var create = Charge.Create(facilityId, patientId, chargeCode, description, amount, currency, encounterId, sourceEventId);
        if (create.IsFailure) return create;

        db.Charges.Add(create.Value!);
        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(),
            "BillableEventCreated",
            "v1",
            DateTimeOffset.UtcNow,
            null,
            sourceEventId,
            facilityId,
            patientId.ToString(),
            JsonSerializer.Serialize(new
            {
                create.Value!.Id,
                create.Value.PatientId,
                create.Value.ChargeCode,
                create.Value.Amount,
                create.Value.Currency
            })), cancellationToken);

        await auditWriter.WriteAsync("HMS", "PostCharge", nameof(Charge), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public Task<List<Charge>> ListForPatientAsync(Guid patientId, CancellationToken cancellationToken = default) =>
        db.Charges.AsNoTracking().Where(x => x.PatientId == patientId).OrderByDescending(x => x.CreatedAt).ToListAsync(cancellationToken);
}
""",
)

w(
    "src/Modules/Hms/HealthcareERP.Modules.Hms/DependencyInjection.cs",
    """
using HealthcareERP.Modules.Hms.Persistence;
using HealthcareERP.Modules.Hms.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace HealthcareERP.Modules.Hms;

public static class DependencyInjection
{
    public static IServiceCollection AddHmsModule(this IServiceCollection services, string? connectionString, bool useInMemory = false)
    {
        if (useInMemory || string.IsNullOrWhiteSpace(connectionString))
            services.AddDbContext<HmsDbContext>(o => o.UseInMemoryDatabase("healthcare-erp-hms"));
        else
            services.AddDbContext<HmsDbContext>(o => o.UseNpgsql(connectionString));

        services.AddScoped<PatientService>();
        services.AddScoped<AppointmentService>();
        services.AddScoped<BillingService>();
        services.AddScoped<OpdService>();
        return services;
    }
}
""",
)

# Stub modules DI
for mod, ns in [
    ("Financials", "HealthcareERP.Modules.Financials"),
    ("Inventory", "HealthcareERP.Modules.Inventory"),
    ("Procurement", "HealthcareERP.Modules.Procurement"),
    ("Hris", "HealthcareERP.Modules.Hris"),
]:
    w(
        f"src/Modules/{mod}/{ns}/{ns.split('.')[-1] if False else ''}DependencyInjection.cs".replace("//", "/"),
        f"""
using Microsoft.Extensions.DependencyInjection;

namespace {ns};

public static class DependencyInjection
{{
    public static IServiceCollection Add{mod}Module(this IServiceCollection services)
    {{
        // Module shell — implement after requirements gate for this increment.
        return services;
    }}
}}
""",
    )

# Fix stub paths - I made a mess. Rewrite properly.
for mod in ["Financials", "Inventory", "Procurement", "Hris"]:
    w(
        f"src/Modules/{mod}/HealthcareERP.Modules.{mod}/DependencyInjection.cs",
        f"""
using Microsoft.Extensions.DependencyInjection;

namespace HealthcareERP.Modules.{mod};

public static class DependencyInjection
{{
    public static IServiceCollection Add{mod}Module(this IServiceCollection services)
    {{
        // Module shell reserved for the corresponding build increment.
        return services;
    }}
}}
""",
    )

# Host
w(
    "src/Host/HealthcareERP.Api/Services/CurrentUser.cs",
    """
using System.Security.Claims;
using HealthcareERP.BuildingBlocks.Application.Abstractions;

namespace HealthcareERP.Api.Services;

public sealed class CurrentUser(IHttpContextAccessor accessor) : ICurrentUser
{
    public Guid? UserId => Guid.TryParse(accessor.HttpContext?.User.FindFirstValue(ClaimTypes.NameIdentifier), out var id) ? id : null;
    public string? UserName => accessor.HttpContext?.User.Identity?.Name ?? accessor.HttpContext?.User.FindFirstValue("name");
    public Guid? FacilityId => Guid.TryParse(accessor.HttpContext?.Request.Headers["X-Facility-Id"], out var id) ? id : null;
    public bool IsAuthenticated => accessor.HttpContext?.User?.Identity?.IsAuthenticated == true;
}
""",
)

w(
    "src/Host/HealthcareERP.Api/Controllers/FacilitiesController.cs",
    """
using HealthcareERP.Modules.Foundation.Services;
using Microsoft.AspNetCore.Mvc;

namespace HealthcareERP.Api.Controllers;

[ApiController]
[Route("api/fnd/facilities")]
public sealed class FacilitiesController(FacilityService facilityService) : ControllerBase
{
    public sealed record CreateFacilityRequest(string Code, string Name, string Timezone, string Currency);
    public sealed record CreateOrgUnitRequest(string Code, string Name, string Type, Guid? ParentId, Guid? CostCenterRef);

    [HttpGet]
    public async Task<IActionResult> List(CancellationToken cancellationToken) =>
        Ok(await facilityService.ListAsync(cancellationToken));

    [HttpPost]
    public async Task<IActionResult> Create([FromBody] CreateFacilityRequest request, CancellationToken cancellationToken)
    {
        var result = await facilityService.CreateAsync(request.Code, request.Name, request.Timezone, request.Currency, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpGet("{facilityId:guid}/org-units")]
    public async Task<IActionResult> ListOrgUnits(Guid facilityId, CancellationToken cancellationToken) =>
        Ok(await facilityService.ListOrgUnitsAsync(facilityId, cancellationToken));

    [HttpPost("{facilityId:guid}/org-units")]
    public async Task<IActionResult> CreateOrgUnit(Guid facilityId, [FromBody] CreateOrgUnitRequest request, CancellationToken cancellationToken)
    {
        var result = await facilityService.CreateOrgUnitAsync(facilityId, request.Code, request.Name, request.Type, request.ParentId, request.CostCenterRef, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }
}
""",
)

w(
    "src/Host/HealthcareERP.Api/Controllers/PatientsController.cs",
    """
using HealthcareERP.Modules.Hms.Services;
using Microsoft.AspNetCore.Mvc;

namespace HealthcareERP.Api.Controllers;

[ApiController]
[Route("api/hms/patients")]
public sealed class PatientsController(PatientService patientService) : ControllerBase
{
    public sealed record RegisterPatientRequest(
        Guid FacilityId,
        string Mrn,
        string FirstName,
        string LastName,
        DateOnly? DateOfBirth,
        string? Phone,
        string? NationalId);

    [HttpGet]
    public async Task<IActionResult> Search([FromQuery] Guid facilityId, [FromQuery] string? query, CancellationToken cancellationToken) =>
        Ok(await patientService.SearchAsync(facilityId, query, cancellationToken));

    [HttpPost]
    public async Task<IActionResult> Register([FromBody] RegisterPatientRequest request, CancellationToken cancellationToken)
    {
        var result = await patientService.RegisterAsync(
            request.FacilityId, request.Mrn, request.FirstName, request.LastName,
            request.DateOfBirth, request.Phone, request.NationalId, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }
}
""",
)

w(
    "src/Host/HealthcareERP.Api/Controllers/AppointmentsController.cs",
    """
using HealthcareERP.Modules.Hms.Services;
using Microsoft.AspNetCore.Mvc;

namespace HealthcareERP.Api.Controllers;

[ApiController]
[Route("api/hms/appointments")]
public sealed class AppointmentsController(AppointmentService appointmentService) : ControllerBase
{
    public sealed record ScheduleRequest(
        Guid FacilityId,
        Guid PatientId,
        Guid ClinicianEmployeeId,
        DateTimeOffset StartsAt,
        DateTimeOffset EndsAt,
        Guid? ClinicOrgUnitId,
        string? Reason);

    [HttpGet]
    public async Task<IActionResult> List([FromQuery] Guid facilityId, [FromQuery] DateOnly date, CancellationToken cancellationToken) =>
        Ok(await appointmentService.ListAsync(facilityId, date, cancellationToken));

    [HttpPost]
    public async Task<IActionResult> Schedule([FromBody] ScheduleRequest request, CancellationToken cancellationToken)
    {
        var result = await appointmentService.ScheduleAsync(
            request.FacilityId, request.PatientId, request.ClinicianEmployeeId,
            request.StartsAt, request.EndsAt, request.ClinicOrgUnitId, request.Reason, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("{id:guid}/check-in")]
    public async Task<IActionResult> CheckIn(Guid id, CancellationToken cancellationToken)
    {
        var result = await appointmentService.CheckInAsync(id, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }
}
""",
)

w(
    "src/Host/HealthcareERP.Api/Controllers/OpdController.cs",
    """
using HealthcareERP.Modules.Hms.Services;
using Microsoft.AspNetCore.Mvc;

namespace HealthcareERP.Api.Controllers;

[ApiController]
[Route("api/hms/opd/encounters")]
public sealed class OpdController(OpdService opdService) : ControllerBase
{
    public sealed record OpenEncounterRequest(Guid FacilityId, Guid PatientId, Guid ClinicianEmployeeId, Guid? AppointmentId, string? ChiefComplaint);
    public sealed record CloseEncounterRequest(string Disposition, decimal ConsultationFee, string Currency);

    [HttpPost]
    public async Task<IActionResult> Open([FromBody] OpenEncounterRequest request, CancellationToken cancellationToken)
    {
        var result = await opdService.OpenAsync(request.FacilityId, request.PatientId, request.ClinicianEmployeeId, request.AppointmentId, request.ChiefComplaint, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("{id:guid}/close")]
    public async Task<IActionResult> Close(Guid id, [FromBody] CloseEncounterRequest request, CancellationToken cancellationToken)
    {
        var result = await opdService.CloseAsync(id, request.Disposition, request.ConsultationFee, request.Currency, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }
}
""",
)

w(
    "src/Host/HealthcareERP.Api/Controllers/BillingController.cs",
    """
using HealthcareERP.Modules.Hms.Services;
using Microsoft.AspNetCore.Mvc;

namespace HealthcareERP.Api.Controllers;

[ApiController]
[Route("api/hms/billing")]
public sealed class BillingController(BillingService billingService) : ControllerBase
{
    [HttpGet("patients/{patientId:guid}/charges")]
    public async Task<IActionResult> ListCharges(Guid patientId, CancellationToken cancellationToken) =>
        Ok(await billingService.ListForPatientAsync(patientId, cancellationToken));
}
""",
)

w(
    "src/Host/HealthcareERP.Api/Controllers/HealthController.cs",
    """
using Microsoft.AspNetCore.Mvc;

namespace HealthcareERP.Api.Controllers;

[ApiController]
[Route("api/health")]
public sealed class HealthController : ControllerBase
{
    [HttpGet]
    public IActionResult Get() => Ok(new
    {
        status = "Healthy",
        service = "HealthcareERP.Api",
        utc = DateTimeOffset.UtcNow
    });
}
""",
)

w(
    "src/Host/HealthcareERP.Api/Program.cs",
    """
using HealthcareERP.Api.Services;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.Modules.Financials;
using HealthcareERP.Modules.Foundation;
using HealthcareERP.Modules.Hms;
using HealthcareERP.Modules.Hris;
using HealthcareERP.Modules.Inventory;
using HealthcareERP.Modules.Procurement;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddHttpContextAccessor();
builder.Services.AddScoped<ICurrentUser, CurrentUser>();

var useInMemory = builder.Configuration.GetValue("Database:UseInMemory", true);
var connectionString = builder.Configuration.GetConnectionString("Default");

builder.Services.AddFoundationModule(connectionString, useInMemory);
builder.Services.AddHmsModule(connectionString, useInMemory);
builder.Services.AddHrisModule();
builder.Services.AddFinancialsModule();
builder.Services.AddInventoryModule();
builder.Services.AddProcurementModule();

builder.Services.AddCors(options =>
{
    options.AddPolicy("frontend", policy =>
        policy.AllowAnyHeader().AllowAnyMethod().WithOrigins("http://localhost:5173", "http://127.0.0.1:5173"));
});

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI();
app.UseCors("frontend");
app.MapControllers();
app.Run();

public partial class Program;
""",
)

w(
    "src/Host/HealthcareERP.Api/appsettings.json",
    """
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*",
  "Database": {
    "UseInMemory": true
  },
  "ConnectionStrings": {
    "Default": "Host=localhost;Port=5432;Database=healthcare_erp;Username=postgres;Password=postgres"
  }
}
""",
)

w(
    "src/Host/HealthcareERP.Api/appsettings.Development.json",
    """
{
  "Database": {
    "UseInMemory": true
  }
}
""",
)

# Tests
w(
    "tests/HealthcareERP.UnitTests/FacilityTests.cs",
    """
using FluentAssertions;
using HealthcareERP.Modules.Foundation.Domain;

namespace HealthcareERP.UnitTests;

public class FacilityTests
{
    [Fact]
    public void Create_WithValidData_Succeeds()
    {
        var result = Facility.Create("MAIN", "Main Hospital", "Asia/Karachi", "PKR");
        result.IsSuccess.Should().BeTrue();
        result.Value!.Code.Should().Be("MAIN");
        result.Value.Status.Should().Be("Active");
    }

    [Fact]
    public void Create_WithInvalidCurrency_Fails()
    {
        var result = Facility.Create("MAIN", "Main Hospital", "UTC", "RUPEE");
        result.IsFailure.Should().BeTrue();
    }
}
""",
)

w(
    "tests/HealthcareERP.UnitTests/PatientTests.cs",
    """
using FluentAssertions;
using HealthcareERP.Modules.Hms.Domain;

namespace HealthcareERP.UnitTests;

public class PatientTests
{
    [Fact]
    public void Register_RequiresNamesAndMrn()
    {
        var ok = Patient.Register(Guid.NewGuid(), "MRN001", "Ali", "Khan", null, null, null);
        ok.IsSuccess.Should().BeTrue();

        var bad = Patient.Register(Guid.NewGuid(), "", "Ali", "Khan", null, null, null);
        bad.IsFailure.Should().BeTrue();
    }
}
""",
)

w(
    "tests/HealthcareERP.ArchitectureTests/ModuleBoundaryTests.cs",
    """
using NetArchTest.Rules;

namespace HealthcareERP.ArchitectureTests;

public class ModuleBoundaryTests
{
    [Fact]
    public void Hms_Should_Not_Reference_Other_Module_Implementations()
    {
        var result = Types.InAssembly(typeof(HealthcareERP.Modules.Hms.DependencyInjection).Assembly)
            .ShouldNot()
            .HaveDependencyOnAny(
                "HealthcareERP.Modules.Financials",
                "HealthcareERP.Modules.Inventory",
                "HealthcareERP.Modules.Procurement",
                "HealthcareERP.Modules.Hris")
            .GetResult();

        Assert.True(result.IsSuccessful, string.Join(", ", result.FailingTypeNames ?? []));
    }

    [Fact]
    public void Inventory_Should_Not_Reference_Hms_Implementation()
    {
        var result = Types.InAssembly(typeof(HealthcareERP.Modules.Inventory.DependencyInjection).Assembly)
            .ShouldNot()
            .HaveDependencyOn("HealthcareERP.Modules.Hms")
            .GetResult();

        Assert.True(result.IsSuccessful, string.Join(", ", result.FailingTypeNames ?? []));
    }
}
""",
)

w(
    "tests/HealthcareERP.IntegrationTests/HealthEndpointTests.cs",
    """
using System.Net;
using FluentAssertions;
using Microsoft.AspNetCore.Mvc.Testing;

namespace HealthcareERP.IntegrationTests;

public class HealthEndpointTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory;

    public HealthEndpointTests(WebApplicationFactory<Program> factory) => _factory = factory;

    [Fact]
    public async Task Health_Returns_Ok()
    {
        var client = _factory.CreateClient();
        var response = await client.GetAsync("/api/health");
        response.StatusCode.Should().Be(HttpStatusCode.OK);
    }
}
""",
)

# Remove default unit test files
for p in ROOT.rglob("UnitTest1.cs"):
    p.unlink()

w(
    ".gitignore",
    """
## .NET
bin/
obj/
*.user
*.suo
.vs/
*.DotSettings.user

## Node
node_modules/
dist/
frontend/dist/
.npm/

## Secrets / local
appsettings.*.local.json
.env
.env.*

## OS / IDE
.DS_Store
Thumbs.db
.idea/
.vscode/*
!.vscode/extensions.json

## Python
__pycache__/
*.pyc

## Test / coverage
TestResults/
coverage/
""",
)

w(
    "README.md",
    """
# Healthcare ERP (Modular Monolith)

Integrated Healthcare Enterprise Software covering **HMS, HRIS, Financials, Inventory, Procurement**, and a shared **Foundation** integration hub.

## Documentation
- Blueprint: [`Healthcare-ERP-Pathway-and-Workflow.md`](Healthcare-ERP-Pathway-and-Workflow.md)
- Requirements library: [`docs/requirements/README.md`](docs/requirements/README.md)
- Verification package: [`docs/requirements/VERIFICATION.md`](docs/requirements/VERIFICATION.md)
- Architecture ADRs: [`docs/architecture/`](docs/architecture/)

## Stack
| Layer | Choice |
|---|---|
| API | ASP.NET Core (`net9.0`, bump path to `net10.0` — see ADR-001) |
| UI | React + TypeScript (Vite) |
| DB | PostgreSQL (InMemory enabled for local demo by default) |
| Architecture | Modular monolith + outbox/inbox integration events |

## Solution layout
```
src/
  BuildingBlocks/
  Host/HealthcareERP.Api/
  Modules/{Foundation,Hms,Hris,Financials,Inventory,Procurement}/
frontend/
docs/requirements/
tests/
```

## Quick start (API)
```bash
dotnet restore HealthcareERP.sln
dotnet test HealthcareERP.sln
dotnet run --project src/Host/HealthcareERP.Api
```
Swagger UI: `http://localhost:5xxx/swagger` (see console for port)

Default `Database:UseInMemory=true` so PostgreSQL is not required for the first demo.

## Quick start (Frontend)
```bash
cd frontend
npm install
npm run dev
```

## Build increments (gated)
1. Foundation hub — **implemented (MVP)**
2. HMS core (registration, appointments, OPD, billing charges) — **implemented (MVP)**
3. Financials core — shell ready
4. Inventory — shell ready
5. Procurement — shell ready
6. Remaining HMS operational sub-modules
7. HRIS
8. Optimization / portals / MIS

Each increment maps to requirement IDs under `docs/requirements/` and stops for acceptance review.
""",
)

w(
    "docs/architecture/ACCEPTANCE-INCREMENT-01.md",
    """
# Acceptance Checklist — Increment 1 (Foundation + HMS Core)

## Requirement coverage
| Area | Specs | Implemented |
|---|---|---|
| Facilities / org units | FND-TEN-* | Create/list facility + org units APIs |
| Audit write | FND-AUD-* | AuditWriter on create paths |
| Outbox | FND-EVT-* | Outbox table + background dispatcher |
| Patient registration | HMS-FO-* | Register/search patients |
| Appointments | HMS-FO-* | Schedule/list/check-in |
| OPD | HMS-OPD-* | Open/close encounter |
| Billing charges | HMS-BIL-* | Idempotent charge posting on OPD close |

## Automated verification
- [ ] `dotnet test` passes (unit + architecture + integration health)
- [ ] `/api/health` returns Healthy
- [ ] Can create facility, register patient, schedule appointment, check-in, open/close OPD with charge

## Known limitations
- Auth is stubbed (CurrentUser reads headers/claims; JWT wiring next)
- PostgreSQL migrations not yet generated (InMemory default)
- HRIS credential gate not yet enforced on scheduling
- Financials AR consumer of `BillableEventCreated` not yet implemented
- React UI is a thin operational console for the MVP paths

## Sign-off
| Role | Decision | Date |
|---|---|---|
| Product Owner | Approve / Amend | |
""",
)

print("modules+host done")
