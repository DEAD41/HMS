using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hris.Domain;

public sealed class RosterAssignment : AggregateRoot
{
    private RosterAssignment() { }

    public Guid FacilityId { get; private set; }
    public Guid EmployeeId { get; private set; }
    public string Department { get; private set; } = string.Empty;
    public string ShiftCode { get; private set; } = string.Empty;
    public DateOnly DutyDate { get; private set; }
    public string Status { get; private set; } = "Published";

    public static Result<RosterAssignment> Publish(
        Guid facilityId,
        Guid employeeId,
        string department,
        string shiftCode,
        DateOnly dutyDate)
    {
        if (employeeId == Guid.Empty) return Result.Failure<RosterAssignment>("Employee is required.");
        if (string.IsNullOrWhiteSpace(shiftCode)) return Result.Failure<RosterAssignment>("Shift code is required.");

        return Result.Success(new RosterAssignment
        {
            FacilityId = facilityId,
            EmployeeId = employeeId,
            Department = department.Trim(),
            ShiftCode = shiftCode.Trim().ToUpperInvariant(),
            DutyDate = dutyDate,
            Status = "Published"
        });
    }
}
