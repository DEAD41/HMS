using HealthcareERP.Modules.Hms.Integration;
using HealthcareERP.Modules.Hms.Persistence;
using HealthcareERP.Modules.Hms.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace HealthcareERP.Modules.Hms;

public static class DependencyInjection
{
    public static IServiceCollection AddHmsModule(this IServiceCollection services, string? connectionString, bool useInMemory = false)
    {
        if (useInMemory || string.IsNullOrWhiteSpace(connectionString))
            services.AddDbContext<HmsDbContext>(o => o.UseInMemoryDatabase("healthcare-erp-hms"));
        else
            services.AddDbContext<HmsDbContext>(o => o.UseNpgsql(connectionString));

        services.AddScoped<PatientService>();
        services.AddScoped<AppointmentService>();
        services.AddScoped<BillingService>();
        services.AddScoped<OpdService>();
        services.AddScoped<IpdService>();
        services.AddScoped<NursingService>();
        services.AddScoped<EmergencyService>();
        services.AddScoped<OtService>();
        services.AddScoped<LisService>();
        services.AddScoped<RisService>();
        services.AddScoped<PharmacyService>();
        services.AddScoped<DischargeService>();
        services.AddSingleton<ILabAnalyzerAdapter, StubLabAnalyzerAdapter>();
        services.AddSingleton<IPacsAdapter, StubPacsAdapter>();
        return services;
    }
}
