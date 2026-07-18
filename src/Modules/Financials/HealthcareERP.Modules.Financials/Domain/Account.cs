using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Financials.Domain;

public sealed class Account : AggregateRoot
{
    private Account() { }

    public Guid FacilityId { get; private set; }
    public string Code { get; private set; } = string.Empty;
    public string Name { get; private set; } = string.Empty;
    public string Type { get; private set; } = "Asset";
    public string Status { get; private set; } = "Active";

    public static Result<Account> Create(Guid facilityId, string code, string name, string type)
    {
        var allowed = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
            { "Asset", "Liability", "Equity", "Revenue", "Expense" };
        if (facilityId == Guid.Empty) return Result.Failure<Account>("Facility is required.");
        if (string.IsNullOrWhiteSpace(code)) return Result.Failure<Account>("Account code is required.");
        if (string.IsNullOrWhiteSpace(name)) return Result.Failure<Account>("Account name is required.");
        if (!allowed.Contains(type)) return Result.Failure<Account>("Invalid account type.");

        return Result.Success(new Account
        {
            FacilityId = facilityId,
            Code = code.Trim().ToUpperInvariant(),
            Name = name.Trim(),
            Type = type,
            Status = "Active"
        });
    }
}
