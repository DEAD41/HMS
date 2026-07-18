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
