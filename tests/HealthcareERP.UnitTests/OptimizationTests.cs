using FluentAssertions;
using HealthcareERP.Modules.Financials.Domain;
using HealthcareERP.Modules.Foundation.Domain;
using HealthcareERP.Modules.Foundation.Services;
using HealthcareERP.Modules.Procurement.Domain;

namespace HealthcareERP.UnitTests;

public class OptimizationTests
{
    [Fact]
    public void AppUser_HashesAndCreatesWithRoles()
    {
        var user = AppUser.Create("admin", "Admin", AuthService.HashPassword("Admin@123"), ["Admin", "Finance"]);
        user.IsSuccess.Should().BeTrue();
        user.Value!.Roles.Should().Contain(["Admin", "Finance"]);
        user.Value.PasswordHash.Should().Be(AuthService.HashPassword("Admin@123"));
    }

    [Fact]
    public void BudgetLine_TracksOverBudget()
    {
        var line = BudgetLine.Create(Guid.NewGuid(), Guid.NewGuid(), "2026-Q3", "OPEX", 1000m);
        line.IsSuccess.Should().BeTrue();
        line.Value!.Activate().IsSuccess.Should().BeTrue();
        line.Value.RecordActual(1200m).IsSuccess.Should().BeTrue();
        line.Value.IsOverBudget().Should().BeTrue();
        line.Value.UtilizationPercent.Should().Be(120m);
    }

    [Fact]
    public void VendorScorecard_MarksNonCompliantBelowThreshold()
    {
        var card = VendorScorecard.Publish(Guid.NewGuid(), Guid.NewGuid(), "2026-07", 2, 5000m, 40m, 50m);
        card.IsSuccess.Should().BeTrue();
        card.Value!.ComplianceStatus.Should().Be("NonCompliant");
        card.Value.OverallScore.Should().Be(45m);
    }
}
