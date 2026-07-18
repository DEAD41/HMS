using HealthcareERP.BuildingBlocks.Infrastructure.Outbox;
using HealthcareERP.Modules.Financials.Integration;
using HealthcareERP.Modules.Financials.Persistence;
using HealthcareERP.Modules.Financials.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace HealthcareERP.Modules.Financials;

public static class DependencyInjection
{
    public static IServiceCollection AddFinancialsModule(this IServiceCollection services, string? connectionString, bool useInMemory = false)
    {
        if (useInMemory || string.IsNullOrWhiteSpace(connectionString))
            services.AddDbContext<FinancialsDbContext>(o => o.UseInMemoryDatabase("healthcare-erp-fin"));
        else
            services.AddDbContext<FinancialsDbContext>(o => o.UseNpgsql(connectionString));

        services.AddScoped<LedgerService>();
        services.AddScoped<ReceivableService>();
        services.AddScoped<AccountsPayableService>();
        services.AddScoped<BudgetService>();
        services.AddScoped<MisService>();
        services.AddScoped<IIntegrationEventHandler, BillableEventCreatedHandler>();
        services.AddScoped<IIntegrationEventHandler, PayrollPostedHandler>();
        return services;
    }
}
