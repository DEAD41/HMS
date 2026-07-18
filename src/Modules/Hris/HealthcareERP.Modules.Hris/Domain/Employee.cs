using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hris.Domain;

public sealed class Employee : AggregateRoot
{
    private Employee() { }

    public Guid FacilityId { get; private set; }
    public string EmployeeCode { get; private set; } = string.Empty;
    public string FirstName { get; private set; } = string.Empty;
    public string LastName { get; private set; } = string.Empty;
    public string Department { get; private set; } = string.Empty;
    public string JobTitle { get; private set; } = string.Empty;
    public Guid? ManagerEmployeeId { get; private set; }
    public Guid? CostCenterRef { get; private set; }
    public string Status { get; private set; } = "Onboarding";
    public DateOnly JoinDate { get; private set; }

    public string FullName => $"{FirstName} {LastName}".Trim();

    public static Result<Employee> Create(
        Guid facilityId,
        string employeeCode,
        string firstName,
        string lastName,
        string department,
        string jobTitle,
        DateOnly joinDate,
        Guid? managerEmployeeId,
        Guid? costCenterRef)
    {
        if (facilityId == Guid.Empty) return Result.Failure<Employee>("Facility is required.");
        if (string.IsNullOrWhiteSpace(employeeCode)) return Result.Failure<Employee>("Employee code is required.");
        if (string.IsNullOrWhiteSpace(firstName) || string.IsNullOrWhiteSpace(lastName))
            return Result.Failure<Employee>("First and last name are required.");

        return Result.Success(new Employee
        {
            FacilityId = facilityId,
            EmployeeCode = employeeCode.Trim().ToUpperInvariant(),
            FirstName = firstName.Trim(),
            LastName = lastName.Trim(),
            Department = department.Trim(),
            JobTitle = jobTitle.Trim(),
            JoinDate = joinDate,
            ManagerEmployeeId = managerEmployeeId,
            CostCenterRef = costCenterRef,
            Status = "Onboarding"
        });
    }

    public Result Activate()
    {
        Status = "Active";
        Touch();
        return Result.Success();
    }

    public Result Exit()
    {
        if (Status == "Exited") return Result.Failure("Employee already exited.");
        Status = "Exited";
        Touch();
        return Result.Success();
    }
}
