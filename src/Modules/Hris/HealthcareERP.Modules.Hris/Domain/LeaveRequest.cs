using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hris.Domain;

public sealed class LeaveRequest : AggregateRoot
{
    private LeaveRequest() { }

    public Guid FacilityId { get; private set; }
    public Guid EmployeeId { get; private set; }
    public string LeaveType { get; private set; } = "Annual";
    public DateOnly StartDate { get; private set; }
    public DateOnly EndDate { get; private set; }
    public string Status { get; private set; } = "Submitted";
    public string? Reason { get; private set; }

    public static Result<LeaveRequest> Submit(
        Guid facilityId,
        Guid employeeId,
        string leaveType,
        DateOnly startDate,
        DateOnly endDate,
        string? reason)
    {
        if (endDate < startDate) return Result.Failure<LeaveRequest>("End date must be on/after start date.");
        return Result.Success(new LeaveRequest
        {
            FacilityId = facilityId,
            EmployeeId = employeeId,
            LeaveType = string.IsNullOrWhiteSpace(leaveType) ? "Annual" : leaveType.Trim(),
            StartDate = startDate,
            EndDate = endDate,
            Reason = reason,
            Status = "Submitted"
        });
    }

    public Result Approve()
    {
        if (Status != "Submitted") return Result.Failure("Only submitted leave can be approved.");
        Status = "Approved";
        Touch();
        return Result.Success();
    }

    public Result Reject()
    {
        if (Status != "Submitted") return Result.Failure("Only submitted leave can be rejected.");
        Status = "Rejected";
        Touch();
        return Result.Success();
    }
}
