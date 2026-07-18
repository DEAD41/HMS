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
