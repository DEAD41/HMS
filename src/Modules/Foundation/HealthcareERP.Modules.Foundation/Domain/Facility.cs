using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Foundation.Domain;

public sealed class Facility : AggregateRoot
{
    private Facility() { }

    public string Code { get; private set; } = string.Empty;
    public string Name { get; private set; } = string.Empty;
    public string Timezone { get; private set; } = "UTC";
    public string Currency { get; private set; } = "USD";
    public string Status { get; private set; } = "Draft";

    public static Result<Facility> Create(string code, string name, string timezone, string currency)
    {
        if (string.IsNullOrWhiteSpace(code)) return Result.Failure<Facility>("Facility code is required.");
        if (string.IsNullOrWhiteSpace(name)) return Result.Failure<Facility>("Facility name is required.");
        if (string.IsNullOrWhiteSpace(timezone)) return Result.Failure<Facility>("Timezone is required.");
        if (string.IsNullOrWhiteSpace(currency) || currency.Length != 3) return Result.Failure<Facility>("Currency must be ISO-4217.");

        var facility = new Facility
        {
            Code = code.Trim().ToUpperInvariant(),
            Name = name.Trim(),
            Timezone = timezone.Trim(),
            Currency = currency.Trim().ToUpperInvariant(),
            Status = "Active"
        };
        return Result.Success(facility);
    }

    public Result Activate()
    {
        Status = "Active";
        Touch();
        return Result.Success();
    }

    public Result Deactivate()
    {
        Status = "Inactive";
        Touch();
        return Result.Success();
    }
}
