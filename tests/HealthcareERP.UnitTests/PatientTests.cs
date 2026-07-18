using FluentAssertions;
using HealthcareERP.Modules.Hms.Domain;

namespace HealthcareERP.UnitTests;

public class PatientTests
{
    [Fact]
    public void Register_RequiresNamesAndMrn()
    {
        var ok = Patient.Register(Guid.NewGuid(), "MRN001", "Ali", "Khan", null, null, null);
        ok.IsSuccess.Should().BeTrue();

        var bad = Patient.Register(Guid.NewGuid(), "", "Ali", "Khan", null, null, null);
        bad.IsFailure.Should().BeTrue();
    }
}
