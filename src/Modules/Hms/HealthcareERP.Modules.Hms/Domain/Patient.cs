using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class Patient : AggregateRoot
{
    private Patient() { }

    public Guid FacilityId { get; private set; }
    public string Mrn { get; private set; } = string.Empty;
    public string FirstName { get; private set; } = string.Empty;
    public string LastName { get; private set; } = string.Empty;
    public DateOnly? DateOfBirth { get; private set; }
    public string? Phone { get; private set; }
    public string? NationalId { get; private set; }
    public string Status { get; private set; } = "Active";

    public string FullName => $"{FirstName} {LastName}".Trim();

    public static Result<Patient> Register(
        Guid facilityId,
        string mrn,
        string firstName,
        string lastName,
        DateOnly? dateOfBirth,
        string? phone,
        string? nationalId)
    {
        if (facilityId == Guid.Empty) return Result.Failure<Patient>("Facility is required.");
        if (string.IsNullOrWhiteSpace(mrn)) return Result.Failure<Patient>("MRN is required.");
        if (string.IsNullOrWhiteSpace(firstName)) return Result.Failure<Patient>("First name is required.");
        if (string.IsNullOrWhiteSpace(lastName)) return Result.Failure<Patient>("Last name is required.");

        return Result.Success(new Patient
        {
            FacilityId = facilityId,
            Mrn = mrn.Trim().ToUpperInvariant(),
            FirstName = firstName.Trim(),
            LastName = lastName.Trim(),
            DateOfBirth = dateOfBirth,
            Phone = phone?.Trim(),
            NationalId = nationalId?.Trim(),
            Status = "Active"
        });
    }
}
