using HealthcareERP.Modules.Hris.Contracts;
using HealthcareERP.Modules.Hris.Persistence;
using HealthcareERP.Modules.Hris.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace HealthcareERP.Modules.Hris;

public static class DependencyInjection
{
    public static IServiceCollection AddHrisModule(this IServiceCollection services, string? connectionString, bool useInMemory = false)
    {
        if (useInMemory || string.IsNullOrWhiteSpace(connectionString))
            services.AddDbContext<HrisDbContext>(o => o.UseInMemoryDatabase("healthcare-erp-hris"));
        else
            services.AddDbContext<HrisDbContext>(o => o.UseNpgsql(connectionString));

        services.AddScoped<EmployeeService>();
        services.AddScoped<CredentialService>();
        services.AddScoped<ICredentialStatusQuery>(sp => sp.GetRequiredService<CredentialService>());
        services.AddScoped<RosterService>();
        services.AddScoped<LeaveService>();
        services.AddScoped<PayrollService>();
        services.AddScoped<EssService>();
        return services;
    }
}
