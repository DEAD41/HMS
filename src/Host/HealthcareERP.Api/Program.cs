using System.Text;
using HealthcareERP.Api.Services;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.Modules.Financials;
using HealthcareERP.Modules.Financials.Persistence;
using HealthcareERP.Modules.Foundation;
using HealthcareERP.Modules.Foundation.Persistence;
using HealthcareERP.Modules.Foundation.Services;
using HealthcareERP.Modules.Hms;
using HealthcareERP.Modules.Hms.Persistence;
using HealthcareERP.Modules.Hris;
using HealthcareERP.Modules.Hris.Persistence;
using HealthcareERP.Modules.Inventory;
using HealthcareERP.Modules.Inventory.Persistence;
using HealthcareERP.Modules.Procurement;
using HealthcareERP.Modules.Procurement.Persistence;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo { Title = "Healthcare ERP API", Version = "v1" });
    options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Description = "JWT Authorization header using the Bearer scheme. Example: Bearer {token}",
        Name = "Authorization",
        In = ParameterLocation.Header,
        Type = SecuritySchemeType.Http,
        Scheme = "bearer",
        BearerFormat = "JWT"
    });
    options.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference { Type = ReferenceType.SecurityScheme, Id = "Bearer" }
            },
            Array.Empty<string>()
        }
    });
});
builder.Services.AddHttpContextAccessor();
builder.Services.AddScoped<ICurrentUser, CurrentUser>();
builder.Services.AddSingleton<JwtTokenService>();

var jwtKey = builder.Configuration["Auth:JwtKey"] ?? "HealthcareERP-Dev-Signing-Key-Change-In-Production-32+";
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["Auth:Issuer"] ?? "HealthcareERP",
            ValidAudience = builder.Configuration["Auth:Audience"] ?? "HealthcareERP",
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtKey))
        };
    });
builder.Services.AddAuthorization();

var useInMemory = builder.Configuration.GetValue("Database:UseInMemory", true);
string? Conn(string name) =>
    builder.Configuration.GetConnectionString(name) ?? builder.Configuration.GetConnectionString("Default");

builder.Services.AddFoundationModule(Conn("Foundation"), useInMemory);
builder.Services.AddHmsModule(Conn("Hms"), useInMemory);
builder.Services.AddHrisModule(Conn("Hris"), useInMemory);
builder.Services.AddFinancialsModule(Conn("Financials"), useInMemory);
builder.Services.AddInventoryModule(Conn("Inventory"), useInMemory);
builder.Services.AddProcurementModule(Conn("Procurement"), useInMemory);

builder.Services.AddCors(options =>
{
    options.AddPolicy("frontend", policy =>
        policy.AllowAnyHeader().AllowAnyMethod().WithOrigins("http://localhost:5173", "http://127.0.0.1:5173"));
});

var app = builder.Build();

await InitializeDatabasesAsync(app);

app.UseSwagger();
app.UseSwaggerUI();
app.UseCors("frontend");
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
app.Run();

static async Task InitializeDatabasesAsync(WebApplication app)
{
    const int maxAttempts = 10;

    for (var attempt = 1; attempt <= maxAttempts; attempt++)
    {
        try
        {
            await using var scope = app.Services.CreateAsyncScope();
            var sp = scope.ServiceProvider;
            await sp.GetRequiredService<FoundationDbContext>().Database.EnsureCreatedAsync();
            await sp.GetRequiredService<HmsDbContext>().Database.EnsureCreatedAsync();
            await sp.GetRequiredService<HrisDbContext>().Database.EnsureCreatedAsync();
            await sp.GetRequiredService<FinancialsDbContext>().Database.EnsureCreatedAsync();
            await sp.GetRequiredService<InventoryDbContext>().Database.EnsureCreatedAsync();
            await sp.GetRequiredService<ProcurementDbContext>().Database.EnsureCreatedAsync();
            await sp.GetRequiredService<AuthService>().SeedDemoUsersAsync();
            return;
        }
        catch when (attempt < maxAttempts)
        {
            await Task.Delay(TimeSpan.FromSeconds(2));
        }
    }
}

public partial class Program;
