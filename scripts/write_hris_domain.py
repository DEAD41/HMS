#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def w(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print("wrote", rel)


w(
    "src/Modules/Hris/HealthcareERP.Modules.Hris.Contracts/ICredentialStatusQuery.cs",
    """
namespace HealthcareERP.Modules.Hris.Contracts;

public interface ICredentialStatusQuery
{
    Task<bool> IsClinicianSchedulableAsync(Guid employeeId, Guid facilityId, CancellationToken cancellationToken = default);
}
""",
)

w(
    "src/Modules/Hris/HealthcareERP.Modules.Hris.Contracts/Events/EmployeeChanged.cs",
    """
namespace HealthcareERP.Modules.Hris.Contracts.Events;

public sealed record EmployeeChanged(Guid EmployeeId, string EmployeeCode, string FullName, string Status);
""",
)

w(
    "src/Modules/Hris/HealthcareERP.Modules.Hris.Contracts/Events/EmployeeCredentialStatusChanged.cs",
    """
namespace HealthcareERP.Modules.Hris.Contracts.Events;

public sealed record EmployeeCredentialStatusChanged(Guid EmployeeId, Guid FacilityId, string Status, bool IsSchedulable);
""",
)

w(
    "src/Modules/Hris/HealthcareERP.Modules.Hris.Contracts/Events/PayrollPosted.cs",
    """
namespace HealthcareERP.Modules.Hris.Contracts.Events;

public sealed record PayrollPosted(Guid PayrollRunId, Guid FacilityId, string Period, decimal GrossAmount, decimal NetAmount);
""",
)

w(
    "src/Modules/Hris/HealthcareERP.Modules.Hris/Domain/Employee.cs",
    """
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
""",
)

w(
    "src/Modules/Hris/HealthcareERP.Modules.Hris/Domain/Credential.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hris.Domain;

public sealed class Credential : AggregateRoot
{
    private Credential() { }

    public Guid FacilityId { get; private set; }
    public Guid EmployeeId { get; private set; }
    public string Type { get; private set; } = "License";
    public string Number { get; private set; } = string.Empty;
    public string Specialty { get; private set; } = string.Empty;
    public DateOnly IssueDate { get; private set; }
    public DateOnly ExpiryDate { get; private set; }
    public string Status { get; private set; } = "Submitted";

    public static Result<Credential> Create(
        Guid facilityId,
        Guid employeeId,
        string type,
        string number,
        string specialty,
        DateOnly issueDate,
        DateOnly expiryDate)
    {
        if (employeeId == Guid.Empty) return Result.Failure<Credential>("Employee is required.");
        if (string.IsNullOrWhiteSpace(number)) return Result.Failure<Credential>("Credential number is required.");
        if (expiryDate < issueDate) return Result.Failure<Credential>("Expiry must be on/after issue date.");

        var status = expiryDate < DateOnly.FromDateTime(DateTime.UtcNow) ? "Expired" : "Active";
        return Result.Success(new Credential
        {
            FacilityId = facilityId,
            EmployeeId = employeeId,
            Type = string.IsNullOrWhiteSpace(type) ? "License" : type.Trim(),
            Number = number.Trim(),
            Specialty = specialty.Trim(),
            IssueDate = issueDate,
            ExpiryDate = expiryDate,
            Status = status
        });
    }

    public Result Verify()
    {
        if (ExpiryDate < DateOnly.FromDateTime(DateTime.UtcNow))
        {
            Status = "Expired";
            return Result.Failure("Credential is expired.");
        }
        Status = "Active";
        Touch();
        return Result.Success();
    }

    public bool IsSchedulable => Status == "Active" && ExpiryDate >= DateOnly.FromDateTime(DateTime.UtcNow);
}
""",
)

w(
    "src/Modules/Hris/HealthcareERP.Modules.Hris/Domain/RosterAssignment.cs",
    """
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
""",
)

w(
    "src/Modules/Hris/HealthcareERP.Modules.Hris/Domain/LeaveRequest.cs",
    """
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
""",
)

w(
    "src/Modules/Hris/HealthcareERP.Modules.Hris/Domain/PayrollRun.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hris.Domain;

public sealed class PayrollRun : AggregateRoot
{
    private PayrollRun() { }

    public Guid FacilityId { get; private set; }
    public string Period { get; private set; } = string.Empty;
    public decimal GrossAmount { get; private set; }
    public decimal Deductions { get; private set; }
    public decimal NetAmount { get; private set; }
    public string Status { get; private set; } = "Open";

    public static Result<PayrollRun> Create(Guid facilityId, string period, decimal grossAmount, decimal deductions)
    {
        if (string.IsNullOrWhiteSpace(period)) return Result.Failure<PayrollRun>("Period is required.");
        if (grossAmount < 0 || deductions < 0) return Result.Failure<PayrollRun>("Amounts cannot be negative.");
        if (deductions > grossAmount) return Result.Failure<PayrollRun>("Deductions cannot exceed gross.");

        return Result.Success(new PayrollRun
        {
            FacilityId = facilityId,
            Period = period.Trim(),
            GrossAmount = grossAmount,
            Deductions = deductions,
            NetAmount = grossAmount - deductions,
            Status = "Calculated"
        });
    }

    public Result Post()
    {
        if (Status is not ("Calculated" or "Approved"))
            return Result.Failure("Payroll must be calculated/approved before posting.");
        Status = "Posted";
        Touch();
        return Result.Success();
    }
}
""",
)

print("hris domain done")
