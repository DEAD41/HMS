#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def w(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print("wrote", rel)


w(
    "src/Modules/Hris/HealthcareERP.Modules.Hris/Persistence/HrisDbContext.cs",
    """
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
""",
)

w(
    "src/Modules/Hris/HealthcareERP.Modules.Hris/Services/EmployeeService.cs",
    """
using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hris.Contracts.Events;
using HealthcareERP.Modules.Hris.Domain;
using HealthcareERP.Modules.Hris.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hris.Services;

public sealed class EmployeeService(HrisDbContext db, IIntegrationEventPublisher publisher, IAuditWriter auditWriter)
{
    public async Task<Result<Employee>> CreateAsync(
        Guid facilityId,
        string employeeCode,
        string firstName,
        string lastName,
        string department,
        string jobTitle,
        DateOnly joinDate,
        Guid? managerEmployeeId,
        Guid? costCenterRef,
        CancellationToken cancellationToken = default)
    {
        if (await db.Employees.AnyAsync(x => x.FacilityId == facilityId && x.EmployeeCode == employeeCode.Trim().ToUpperInvariant(), cancellationToken))
            return Result.Failure<Employee>("Employee code already exists.");

        var create = Employee.Create(facilityId, employeeCode, firstName, lastName, department, jobTitle, joinDate, managerEmployeeId, costCenterRef);
        if (create.IsFailure) return create;

        db.Employees.Add(create.Value!);
        await PublishEmployeeChangedAsync(create.Value!, cancellationToken);
        await auditWriter.WriteAsync("HRIS", "Create", nameof(Employee), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<Employee>> ActivateAsync(Guid employeeId, CancellationToken cancellationToken = default)
    {
        var employee = await db.Employees.FirstOrDefaultAsync(x => x.Id == employeeId, cancellationToken);
        if (employee is null) return Result.Failure<Employee>("Employee not found.");
        var activate = employee.Activate();
        if (activate.IsFailure) return Result.Failure<Employee>(activate.Error!);
        await PublishEmployeeChangedAsync(employee, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(employee);
    }

    public async Task<Result<Employee>> ExitAsync(Guid employeeId, CancellationToken cancellationToken = default)
    {
        var employee = await db.Employees.FirstOrDefaultAsync(x => x.Id == employeeId, cancellationToken);
        if (employee is null) return Result.Failure<Employee>("Employee not found.");
        var exit = employee.Exit();
        if (exit.IsFailure) return Result.Failure<Employee>(exit.Error!);
        await PublishEmployeeChangedAsync(employee, cancellationToken);
        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(), "EmployeeExited", "v1", DateTimeOffset.UtcNow, null, null, employee.FacilityId, employee.Id.ToString(),
            JsonSerializer.Serialize(new { employee.Id, employee.EmployeeCode })), cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(employee);
    }

    public Task<List<Employee>> ListAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.Employees.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderBy(x => x.EmployeeCode).ToListAsync(cancellationToken);

    private Task PublishEmployeeChangedAsync(Employee employee, CancellationToken cancellationToken) =>
        publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(), "EmployeeChanged", "v1", DateTimeOffset.UtcNow, null, null, employee.FacilityId, employee.Id.ToString(),
            JsonSerializer.Serialize(new EmployeeChanged(employee.Id, employee.EmployeeCode, employee.FullName, employee.Status))), cancellationToken);
}
""",
)

w(
    "src/Modules/Hris/HealthcareERP.Modules.Hris/Services/CredentialService.cs",
    """
using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hris.Contracts;
using HealthcareERP.Modules.Hris.Contracts.Events;
using HealthcareERP.Modules.Hris.Domain;
using HealthcareERP.Modules.Hris.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hris.Services;

public sealed class CredentialService(HrisDbContext db, IIntegrationEventPublisher publisher, IAuditWriter auditWriter) : ICredentialStatusQuery
{
    public async Task<Result<Credential>> AddAsync(
        Guid facilityId,
        Guid employeeId,
        string type,
        string number,
        string specialty,
        DateOnly issueDate,
        DateOnly expiryDate,
        CancellationToken cancellationToken = default)
    {
        var employee = await db.Employees.FirstOrDefaultAsync(x => x.Id == employeeId && x.FacilityId == facilityId, cancellationToken);
        if (employee is null) return Result.Failure<Credential>("Employee not found.");
        if (employee.Status == "Exited") return Result.Failure<Credential>("Cannot credential an exited employee.");

        var create = Credential.Create(facilityId, employeeId, type, number, specialty, issueDate, expiryDate);
        if (create.IsFailure) return create;
        db.Credentials.Add(create.Value!);

        await PublishStatusAsync(employee, cancellationToken);
        await auditWriter.WriteAsync("HRIS", "AddCredential", nameof(Credential), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<Credential>> VerifyAsync(Guid credentialId, CancellationToken cancellationToken = default)
    {
        var credential = await db.Credentials.FirstOrDefaultAsync(x => x.Id == credentialId, cancellationToken);
        if (credential is null) return Result.Failure<Credential>("Credential not found.");
        var verify = credential.Verify();
        if (verify.IsFailure) return Result.Failure<Credential>(verify.Error!);

        var employee = await db.Employees.FirstAsync(x => x.Id == credential.EmployeeId, cancellationToken);
        await PublishStatusAsync(employee, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(credential);
    }

    public async Task<bool> IsClinicianSchedulableAsync(Guid employeeId, Guid facilityId, CancellationToken cancellationToken = default)
    {
        var employee = await db.Employees.AsNoTracking()
            .FirstOrDefaultAsync(x => x.Id == employeeId && x.FacilityId == facilityId, cancellationToken);
        if (employee is null || employee.Status != "Active") return false;

        return await db.Credentials.AsNoTracking().AnyAsync(x =>
            x.EmployeeId == employeeId &&
            x.FacilityId == facilityId &&
            x.Status == "Active" &&
            x.ExpiryDate >= DateOnly.FromDateTime(DateTime.UtcNow), cancellationToken);
    }

    public Task<List<Credential>> ListForEmployeeAsync(Guid employeeId, CancellationToken cancellationToken = default) =>
        db.Credentials.AsNoTracking().Where(x => x.EmployeeId == employeeId).OrderByDescending(x => x.ExpiryDate).ToListAsync(cancellationToken);

    private async Task PublishStatusAsync(Employee employee, CancellationToken cancellationToken)
    {
        var schedulable = employee.Status == "Active" && await db.Credentials.AnyAsync(x =>
            x.EmployeeId == employee.Id &&
            x.Status == "Active" &&
            x.ExpiryDate >= DateOnly.FromDateTime(DateTime.UtcNow), cancellationToken);

        var status = schedulable ? "Active" : "Inactive";
        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(), "EmployeeCredentialStatusChanged", "v1", DateTimeOffset.UtcNow, null, null, employee.FacilityId, employee.Id.ToString(),
            JsonSerializer.Serialize(new EmployeeCredentialStatusChanged(employee.Id, employee.FacilityId, status, schedulable))), cancellationToken);
    }
}
""",
)

w(
    "src/Modules/Hris/HealthcareERP.Modules.Hris/Services/RosterService.cs",
    """
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hris.Contracts;
using HealthcareERP.Modules.Hris.Domain;
using HealthcareERP.Modules.Hris.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hris.Services;

public sealed class RosterService(HrisDbContext db, ICredentialStatusQuery credentialStatusQuery, IAuditWriter auditWriter)
{
    public async Task<Result<RosterAssignment>> PublishAsync(
        Guid facilityId,
        Guid employeeId,
        string department,
        string shiftCode,
        DateOnly dutyDate,
        CancellationToken cancellationToken = default)
    {
        var employee = await db.Employees.FirstOrDefaultAsync(x => x.Id == employeeId && x.FacilityId == facilityId, cancellationToken);
        if (employee is null) return Result.Failure<RosterAssignment>("Employee not found.");
        if (employee.Status != "Active") return Result.Failure<RosterAssignment>("Only active employees can be rostered.");

        if (!await credentialStatusQuery.IsClinicianSchedulableAsync(employeeId, facilityId, cancellationToken)
            && department.Contains("clinical", StringComparison.OrdinalIgnoreCase))
        {
            return Result.Failure<RosterAssignment>("Employee lacks active clinical credentials for rostering.");
        }

        if (await db.RosterAssignments.AnyAsync(x => x.EmployeeId == employeeId && x.DutyDate == dutyDate && x.ShiftCode == shiftCode.Trim().ToUpperInvariant(), cancellationToken))
            return Result.Failure<RosterAssignment>("Duplicate roster assignment.");

        var create = RosterAssignment.Publish(facilityId, employeeId, department, shiftCode, dutyDate);
        if (create.IsFailure) return create;
        db.RosterAssignments.Add(create.Value!);
        await auditWriter.WriteAsync("HRIS", "PublishRoster", nameof(RosterAssignment), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public Task<List<RosterAssignment>> ListAsync(Guid facilityId, DateOnly? dutyDate, CancellationToken cancellationToken = default)
    {
        var q = db.RosterAssignments.AsNoTracking().Where(x => x.FacilityId == facilityId);
        if (dutyDate is DateOnly d) q = q.Where(x => x.DutyDate == d);
        return q.OrderBy(x => x.DutyDate).ThenBy(x => x.ShiftCode).ToListAsync(cancellationToken);
    }
}
""",
)

w(
    "src/Modules/Hris/HealthcareERP.Modules.Hris/Services/LeaveService.cs",
    """
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hris.Domain;
using HealthcareERP.Modules.Hris.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hris.Services;

public sealed class LeaveService(HrisDbContext db, IAuditWriter auditWriter)
{
    public async Task<Result<LeaveRequest>> SubmitAsync(
        Guid facilityId,
        Guid employeeId,
        string leaveType,
        DateOnly startDate,
        DateOnly endDate,
        string? reason,
        CancellationToken cancellationToken = default)
    {
        if (!await db.Employees.AnyAsync(x => x.Id == employeeId && x.FacilityId == facilityId && x.Status == "Active", cancellationToken))
            return Result.Failure<LeaveRequest>("Active employee required.");

        var overlap = await db.LeaveRequests.AnyAsync(x =>
            x.EmployeeId == employeeId &&
            x.Status == "Approved" &&
            x.StartDate <= endDate &&
            startDate <= x.EndDate, cancellationToken);
        if (overlap) return Result.Failure<LeaveRequest>("Overlapping approved leave exists.");

        var create = LeaveRequest.Submit(facilityId, employeeId, leaveType, startDate, endDate, reason);
        if (create.IsFailure) return create;
        db.LeaveRequests.Add(create.Value!);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<LeaveRequest>> ApproveAsync(Guid leaveId, CancellationToken cancellationToken = default)
    {
        var leave = await db.LeaveRequests.FirstOrDefaultAsync(x => x.Id == leaveId, cancellationToken);
        if (leave is null) return Result.Failure<LeaveRequest>("Leave request not found.");
        var approve = leave.Approve();
        if (approve.IsFailure) return Result.Failure<LeaveRequest>(approve.Error!);
        await auditWriter.WriteAsync("HRIS", "ApproveLeave", nameof(LeaveRequest), leave.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(leave);
    }

    public Task<List<LeaveRequest>> ListAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.LeaveRequests.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderByDescending(x => x.CreatedAt).ToListAsync(cancellationToken);
}
""",
)

w(
    "src/Modules/Hris/HealthcareERP.Modules.Hris/Services/PayrollService.cs",
    """
using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hris.Contracts.Events;
using HealthcareERP.Modules.Hris.Domain;
using HealthcareERP.Modules.Hris.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hris.Services;

public sealed class PayrollService(HrisDbContext db, IIntegrationEventPublisher publisher, IAuditWriter auditWriter)
{
    public async Task<Result<PayrollRun>> CreateAsync(
        Guid facilityId,
        string period,
        decimal grossAmount,
        decimal deductions,
        CancellationToken cancellationToken = default)
    {
        if (await db.PayrollRuns.AnyAsync(x => x.FacilityId == facilityId && x.Period == period.Trim(), cancellationToken))
            return Result.Failure<PayrollRun>("Payroll period already exists.");

        var create = PayrollRun.Create(facilityId, period, grossAmount, deductions);
        if (create.IsFailure) return create;
        db.PayrollRuns.Add(create.Value!);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<PayrollRun>> PostAsync(Guid payrollRunId, CancellationToken cancellationToken = default)
    {
        var run = await db.PayrollRuns.FirstOrDefaultAsync(x => x.Id == payrollRunId, cancellationToken);
        if (run is null) return Result.Failure<PayrollRun>("Payroll run not found.");
        var post = run.Post();
        if (post.IsFailure) return Result.Failure<PayrollRun>(post.Error!);

        var payload = new PayrollPosted(run.Id, run.FacilityId, run.Period, run.GrossAmount, run.NetAmount);
        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(), "PayrollPosted", "v1", DateTimeOffset.UtcNow, null, null, run.FacilityId, run.Id.ToString(),
            JsonSerializer.Serialize(payload)), cancellationToken);

        await auditWriter.WriteAsync("HRIS", "PostPayroll", nameof(PayrollRun), run.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(run);
    }

    public Task<List<PayrollRun>> ListAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.PayrollRuns.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderByDescending(x => x.CreatedAt).ToListAsync(cancellationToken);
}
""",
)

w(
    "src/Modules/Hris/HealthcareERP.Modules.Hris/DependencyInjection.cs",
    """
using HealthcareERP.Modules.Hris.Contracts;
using HealthcareERP.Modules.Hris.Persistence;
using HealthcareERP.Modules.Hris.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace HealthcareERP.Modules.Hris;

public static class DependencyInjection
{
    public static IServiceCollection AddHrisModule(this IServiceCollection services, string? connectionString, bool useInMemory = false)
    {
        if (useInMemory || string.IsNullOrWhiteSpace(connectionString))
            services.AddDbContext<HrisDbContext>(o => o.UseInMemoryDatabase("healthcare-erp-hris"));
        else
            services.AddDbContext<HrisDbContext>(o => o.UseNpgsql(connectionString));

        services.AddScoped<EmployeeService>();
        services.AddScoped<CredentialService>();
        services.AddScoped<ICredentialStatusQuery>(sp => sp.GetRequiredService<CredentialService>());
        services.AddScoped<RosterService>();
        services.AddScoped<LeaveService>();
        services.AddScoped<PayrollService>();
        return services;
    }
}
""",
)

# Financials payroll expense
w(
    "src/Modules/Financials/HealthcareERP.Modules.Financials/Domain/PayrollExpense.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Financials.Domain;

public sealed class PayrollExpense : AggregateRoot
{
    private PayrollExpense() { }

    public Guid FacilityId { get; private set; }
    public Guid PayrollRunId { get; private set; }
    public string Period { get; private set; } = string.Empty;
    public decimal GrossAmount { get; private set; }
    public decimal NetAmount { get; private set; }
    public string Status { get; private set; } = "Posted";

    public static Result<PayrollExpense> FromPayroll(Guid facilityId, Guid payrollRunId, string period, decimal gross, decimal net)
    {
        if (payrollRunId == Guid.Empty) return Result.Failure<PayrollExpense>("Payroll run is required.");
        return Result.Success(new PayrollExpense
        {
            FacilityId = facilityId,
            PayrollRunId = payrollRunId,
            Period = period,
            GrossAmount = gross,
            NetAmount = net,
            Status = "Posted"
        });
    }
}
""",
)

w(
    "src/Modules/Financials/HealthcareERP.Modules.Financials/Integration/PayrollPostedHandler.cs",
    """
using System.Text.Json;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Infrastructure.Outbox;
using HealthcareERP.Modules.Financials.Domain;
using HealthcareERP.Modules.Financials.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Financials.Integration;

public sealed class PayrollPostedHandler(FinancialsDbContext db) : IIntegrationEventHandler
{
    public string EventType => "PayrollPosted";

    public async Task HandleAsync(IntegrationEvent integrationEvent, CancellationToken cancellationToken = default)
    {
        using var doc = JsonDocument.Parse(integrationEvent.PayloadJson);
        var root = doc.RootElement;
        var payrollRunId = root.GetProperty("PayrollRunId").GetGuid();
        if (await db.PayrollExpenses.AnyAsync(x => x.PayrollRunId == payrollRunId, cancellationToken))
            return;

        var period = root.GetProperty("Period").GetString() ?? string.Empty;
        var gross = root.GetProperty("GrossAmount").GetDecimal();
        var net = root.GetProperty("NetAmount").GetDecimal();
        var create = PayrollExpense.FromPayroll(integrationEvent.FacilityId, payrollRunId, period, gross, net);
        if (create.IsFailure) throw new InvalidOperationException(create.Error);

        db.PayrollExpenses.Add(create.Value!);
        await db.SaveChangesAsync(cancellationToken);
    }
}
""",
)

print("hris services done")
