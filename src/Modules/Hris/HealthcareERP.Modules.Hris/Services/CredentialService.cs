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

    public Task<bool> IsClinicianSchedulableAsync(Guid employeeId, Guid facilityId, CancellationToken cancellationToken = default) =>
        HasActiveCredentialAsync(employeeId, facilityId, nursingOnly: false, cancellationToken);

    public Task<bool> IsNurseCapableAsync(Guid employeeId, Guid facilityId, CancellationToken cancellationToken = default) =>
        HasActiveCredentialAsync(employeeId, facilityId, nursingOnly: true, cancellationToken);

    private async Task<bool> HasActiveCredentialAsync(
        Guid employeeId,
        Guid facilityId,
        bool nursingOnly,
        CancellationToken cancellationToken)
    {
        var employee = await db.Employees.AsNoTracking()
            .FirstOrDefaultAsync(x => x.Id == employeeId && x.FacilityId == facilityId, cancellationToken);
        if (employee is null || employee.Status != "Active") return false;

        var today = DateOnly.FromDateTime(DateTime.UtcNow);
        var q = db.Credentials.AsNoTracking().Where(x =>
            x.EmployeeId == employeeId &&
            x.FacilityId == facilityId &&
            x.Status == "Active" &&
            x.ExpiryDate >= today);

        if (nursingOnly)
        {
            q = q.Where(x =>
                x.Specialty.ToLower().Contains("nurs") ||
                x.Type.ToLower().Contains("nurs") ||
                x.Specialty.ToLower() == "rn");
        }

        return await q.AnyAsync(cancellationToken);
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
