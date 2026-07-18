using System.Security.Cryptography;
using System.Text;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Foundation.Domain;
using HealthcareERP.Modules.Foundation.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Foundation.Services;

public sealed class AuthService(FoundationDbContext db, IAuditWriter auditWriter)
{
    public async Task SeedDemoUsersAsync(CancellationToken cancellationToken = default)
    {
        if (await db.Users.AnyAsync(cancellationToken)) return;

        var seeds = new (string User, string Name, string Password, string[] Roles)[]
        {
            ("admin", "System Admin", "Admin@123", ["Admin", "Finance", "Hr", "Clinician", "Employee"]),
            ("doctor", "Demo Doctor", "Doctor@123", ["Clinician", "Employee"]),
            ("hr", "Demo HR Officer", "Hr@123", ["Hr", "Employee"]),
            ("finance", "Demo Finance Controller", "Finance@123", ["Finance", "Employee"]),
            ("employee", "Demo Employee", "Employee@123", ["Employee"]),
        };

        foreach (var seed in seeds)
        {
            var create = AppUser.Create(seed.User, seed.Name, HashPassword(seed.Password), seed.Roles);
            if (create.IsSuccess) db.Users.Add(create.Value!);
        }

        await db.SaveChangesAsync(cancellationToken);
        await auditWriter.WriteAsync("FND", "SeedUsers", nameof(AppUser), Guid.Empty, null, "demo-users", cancellationToken);
    }

    public async Task<Result<AppUser>> LoginAsync(string userName, string password, CancellationToken cancellationToken = default)
    {
        var normalized = userName.Trim().ToLowerInvariant();
        var user = await db.Users.FirstOrDefaultAsync(x => x.UserName == normalized, cancellationToken);
        if (user is null || user.Status != "Active")
            return Result.Failure<AppUser>("Invalid username or password.");
        if (!VerifyPassword(password, user.PasswordHash))
            return Result.Failure<AppUser>("Invalid username or password.");

        await auditWriter.WriteAsync("FND", "Login", nameof(AppUser), user.Id, null, user.UserName, cancellationToken);
        return Result.Success(user);
    }

    public async Task<AppUser?> GetByIdAsync(Guid userId, CancellationToken cancellationToken = default) =>
        await db.Users.AsNoTracking().FirstOrDefaultAsync(x => x.Id == userId, cancellationToken);

    public async Task<Result<AppUser>> LinkEmployeeAsync(Guid userId, Guid employeeId, CancellationToken cancellationToken = default)
    {
        var user = await db.Users.FirstOrDefaultAsync(x => x.Id == userId, cancellationToken);
        if (user is null) return Result.Failure<AppUser>("User not found.");
        var link = user.LinkEmployee(employeeId);
        if (link.IsFailure) return Result.Failure<AppUser>(link.Error!);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(user);
    }

    public Task<List<AppUser>> ListAsync(CancellationToken cancellationToken = default) =>
        db.Users.AsNoTracking().OrderBy(x => x.UserName).ToListAsync(cancellationToken);

    public static string HashPassword(string password)
    {
        var bytes = SHA256.HashData(Encoding.UTF8.GetBytes($"hms-erp|{password}"));
        return Convert.ToHexString(bytes);
    }

    private static bool VerifyPassword(string password, string hash) =>
        string.Equals(HashPassword(password), hash, StringComparison.OrdinalIgnoreCase);
}
