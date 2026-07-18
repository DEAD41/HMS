using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Foundation.Domain;

public sealed class AppUser : AggregateRoot
{
    private AppUser() { }

    public string UserName { get; private set; } = string.Empty;
    public string DisplayName { get; private set; } = string.Empty;
    public string PasswordHash { get; private set; } = string.Empty;
    public string RolesCsv { get; private set; } = "Employee";
    public Guid? EmployeeId { get; private set; }
    public Guid? DefaultFacilityId { get; private set; }
    public string Status { get; private set; } = "Active";

    public IReadOnlyList<string> Roles =>
        RolesCsv.Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);

    public static Result<AppUser> Create(
        string userName,
        string displayName,
        string passwordHash,
        IEnumerable<string> roles,
        Guid? employeeId = null,
        Guid? defaultFacilityId = null)
    {
        if (string.IsNullOrWhiteSpace(userName)) return Result.Failure<AppUser>("Username is required.");
        if (string.IsNullOrWhiteSpace(passwordHash)) return Result.Failure<AppUser>("Password hash is required.");

        var roleList = roles.Select(r => r.Trim()).Where(r => r.Length > 0).Distinct(StringComparer.OrdinalIgnoreCase).ToList();
        if (roleList.Count == 0) roleList.Add("Employee");

        return Result.Success(new AppUser
        {
            UserName = userName.Trim().ToLowerInvariant(),
            DisplayName = displayName.Trim(),
            PasswordHash = passwordHash,
            RolesCsv = string.Join(',', roleList),
            EmployeeId = employeeId,
            DefaultFacilityId = defaultFacilityId,
            Status = "Active"
        });
    }

    public Result LinkEmployee(Guid employeeId)
    {
        if (employeeId == Guid.Empty) return Result.Failure("Employee is required.");
        EmployeeId = employeeId;
        Touch();
        return Result.Success();
    }

    public Result Disable()
    {
        Status = "Disabled";
        Touch();
        return Result.Success();
    }
}
