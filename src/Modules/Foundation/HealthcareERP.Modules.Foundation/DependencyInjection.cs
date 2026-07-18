using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Infrastructure.Outbox;
using HealthcareERP.Modules.Foundation.Persistence;
using HealthcareERP.Modules.Foundation.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace HealthcareERP.Modules.Foundation;

public static class DependencyInjection
{
    public static IServiceCollection AddFoundationModule(this IServiceCollection services, string? connectionString, bool useInMemory = false)
    {
        if (useInMemory || string.IsNullOrWhiteSpace(connectionString))
        {
            services.AddDbContext<FoundationDbContext>(o => o.UseInMemoryDatabase("healthcare-erp"));
        }
        else
        {
            services.AddDbContext<FoundationDbContext>(o => o.UseNpgsql(connectionString));
        }

        services.AddScoped<IIntegrationEventPublisher, EfIntegrationEventPublisher<FoundationDbContext>>();
        services.AddScoped<IAuditWriter, AuditWriter>();
        services.AddScoped<FacilityService>();
        services.AddScoped<AuthService>();
        services.AddHostedService<OutboxDispatcher<FoundationDbContext>>();
        return services;
    }
}
