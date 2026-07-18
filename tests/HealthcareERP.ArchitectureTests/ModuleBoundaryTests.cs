using NetArchTest.Rules;

namespace HealthcareERP.ArchitectureTests;

public class ModuleBoundaryTests
{
    private static readonly string[] ForbiddenHmsCrossModuleImplementationNamespaces =
    [
        "HealthcareERP.Modules.Financials.Domain",
        "HealthcareERP.Modules.Financials.Services",
        "HealthcareERP.Modules.Financials.Persistence",
        "HealthcareERP.Modules.Financials.Integration",
        "HealthcareERP.Modules.Inventory.Domain",
        "HealthcareERP.Modules.Inventory.Services",
        "HealthcareERP.Modules.Inventory.Persistence",
        "HealthcareERP.Modules.Procurement.Domain",
        "HealthcareERP.Modules.Procurement.Services",
        "HealthcareERP.Modules.Procurement.Persistence",
        "HealthcareERP.Modules.Hris.Domain",
        "HealthcareERP.Modules.Hris.Services",
        "HealthcareERP.Modules.Hris.Persistence",
    ];

    [Fact]
    public void Hms_Should_Not_Reference_Other_Module_Implementations()
    {
        var result = Types.InAssembly(typeof(HealthcareERP.Modules.Hms.DependencyInjection).Assembly)
            .ShouldNot()
            .HaveDependencyOnAny(ForbiddenHmsCrossModuleImplementationNamespaces)
            .GetResult();

        Assert.True(result.IsSuccessful, string.Join(", ", result.FailingTypeNames ?? []));
    }

    [Fact]
    public void Inventory_Should_Not_Reference_Hms_Implementation()
    {
        var result = Types.InAssembly(typeof(HealthcareERP.Modules.Inventory.DependencyInjection).Assembly)
            .ShouldNot()
            .HaveDependencyOnAny(
                "HealthcareERP.Modules.Hms.Domain",
                "HealthcareERP.Modules.Hms.Services",
                "HealthcareERP.Modules.Hms.Persistence")
            .GetResult();

        Assert.True(result.IsSuccessful, string.Join(", ", result.FailingTypeNames ?? []));
    }
}
