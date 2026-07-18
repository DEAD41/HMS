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
