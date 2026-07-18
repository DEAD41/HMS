using HealthcareERP.BuildingBlocks.Infrastructure.Outbox;
using HealthcareERP.Modules.Inventory.Integration;
using HealthcareERP.Modules.Inventory.Persistence;
using HealthcareERP.Modules.Inventory.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace HealthcareERP.Modules.Inventory;

public static class DependencyInjection
{
    public static IServiceCollection AddInventoryModule(this IServiceCollection services, string? connectionString, bool useInMemory = false)
    {
        if (useInMemory || string.IsNullOrWhiteSpace(connectionString))
            services.AddDbContext<InventoryDbContext>(o => o.UseInMemoryDatabase("healthcare-erp-inv"));
        else
            services.AddDbContext<InventoryDbContext>(o => o.UseNpgsql(connectionString));

        services.AddScoped<InventoryService>();
        services.AddScoped<IIntegrationEventHandler, MedicationDispensedHandler>();
        return services;
    }
}
