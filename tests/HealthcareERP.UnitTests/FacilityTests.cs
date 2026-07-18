using FluentAssertions;
using HealthcareERP.Modules.Foundation.Domain;

namespace HealthcareERP.UnitTests;

public class FacilityTests
{
    [Fact]
    public void Create_WithValidData_Succeeds()
    {
        var result = Facility.Create("MAIN", "Main Hospital", "Asia/Karachi", "PKR");
        result.IsSuccess.Should().BeTrue();
        result.Value!.Code.Should().Be("MAIN");
        result.Value.Status.Should().Be("Active");
    }

    [Fact]
    public void Create_WithInvalidCurrency_Fails()
    {
        var result = Facility.Create("MAIN", "Main Hospital", "UTC", "RUPEE");
        result.IsFailure.Should().BeTrue();
    }
}
