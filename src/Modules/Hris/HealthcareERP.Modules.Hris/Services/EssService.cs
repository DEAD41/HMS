using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Hris.Domain;
using HealthcareERP.Modules.Hris.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Hris.Services;

public sealed class EssService(HrisDbContext db, LeaveService leaveService, ICurrentUser currentUser)
{
    public async Task<Result<object>> GetMeAsync(CancellationToken cancellationToken = default)
    {
        if (currentUser.EmployeeId is not Guid employeeId)
            return Result.Failure<object>("No employee linked to the current user. Ask Admin to link via /api/fnd/auth/users/{id}/link-employee.");

        var employee = await db.Employees.AsNoTracking().FirstOrDefaultAsync(x => x.Id == employeeId, cancellationToken);
        if (employee is null) return Result.Failure<object>("Employee not found.");

        var credentials = await db.Credentials.AsNoTracking().Where(x => x.EmployeeId == employee.Id).ToListAsync(cancellationToken);
        var leave = await db.LeaveRequests.AsNoTracking().Where(x => x.EmployeeId == employee.Id).OrderByDescending(x => x.CreatedAt).Take(10).ToListAsync(cancellationToken);
        var roster = await db.RosterAssignments.AsNoTracking().Where(x => x.EmployeeId == employee.Id).OrderByDescending(x => x.DutyDate).Take(14).ToListAsync(cancellationToken);
        var payroll = await db.PayrollRuns.AsNoTracking().Where(x => x.FacilityId == employee.FacilityId).OrderByDescending(x => x.CreatedAt).Take(5).ToListAsync(cancellationToken);

        return Result.Success<object>(new
        {
            Employee = employee,
            Credentials = credentials,
            Leave = leave,
            Roster = roster,
            Payslips = payroll.Select(p => new { p.Id, p.Period, p.GrossAmount, p.NetAmount, p.Status })
        });
    }

    public async Task<Result<LeaveRequest>> SubmitLeaveAsync(
        string leaveType,
        DateOnly startDate,
        DateOnly endDate,
        string? reason,
        CancellationToken cancellationToken = default)
    {
        if (currentUser.EmployeeId is not Guid employeeId)
            return Result.Failure<LeaveRequest>("No employee linked to the current user.");

        var employee = await db.Employees.AsNoTracking().FirstOrDefaultAsync(x => x.Id == employeeId, cancellationToken);
        if (employee is null) return Result.Failure<LeaveRequest>("Employee not found.");

        return await leaveService.SubmitAsync(employee.FacilityId, employeeId, leaveType, startDate, endDate, reason, cancellationToken);
    }
}
