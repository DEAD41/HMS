using HealthcareERP.BuildingBlocks.Infrastructure.Outbox;
using HealthcareERP.Modules.Procurement.Integration;
using HealthcareERP.Modules.Procurement.Persistence;
using HealthcareERP.Modules.Procurement.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace HealthcareERP.Modules.Procurement;

public static class DependencyInjection
{
    public static IServiceCollection AddProcurementModule(this IServiceCollection services, string? connectionString, bool useInMemory = false)
    {
        if (useInMemory || string.IsNullOrWhiteSpace(connectionString))
            services.AddDbContext<ProcurementDbContext>(o => o.UseInMemoryDatabase("healthcare-erp-prc"));
        else
            services.AddDbContext<ProcurementDbContext>(o => o.UseNpgsql(connectionString));

        services.AddScoped<ProcurementService>();
        services.AddScoped<VendorPerformanceService>();
        services.AddScoped<IIntegrationEventHandler, PurchaseRequisitionRequestedHandler>();
        return services;
    }
}
