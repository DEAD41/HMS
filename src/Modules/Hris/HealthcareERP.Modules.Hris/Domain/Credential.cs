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

        var status = expiryDate < DateOnly.FromDateTime(DateTime.UtcNow) ? "Expired" : "Submitted";
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
