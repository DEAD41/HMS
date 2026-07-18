using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using HealthcareERP.Modules.Foundation.Domain;
using Microsoft.IdentityModel.Tokens;

namespace HealthcareERP.Api.Services;

public sealed class JwtTokenService(IConfiguration configuration)
{
    public string CreateToken(AppUser user)
    {
        var key = configuration["Auth:JwtKey"] ?? "HealthcareERP-Dev-Signing-Key-Change-In-Production-32+";
        var issuer = configuration["Auth:Issuer"] ?? "HealthcareERP";
        var audience = configuration["Auth:Audience"] ?? "HealthcareERP";
        var hours = configuration.GetValue("Auth:TokenHours", 12);

        var claims = new List<Claim>
        {
            new(ClaimTypes.NameIdentifier, user.Id.ToString()),
            new(ClaimTypes.Name, user.UserName),
            new("display_name", user.DisplayName),
        };

        if (user.DefaultFacilityId is Guid facilityId)
            claims.Add(new Claim("facility_id", facilityId.ToString()));
        if (user.EmployeeId is Guid employeeId)
            claims.Add(new Claim("employee_id", employeeId.ToString()));

        foreach (var role in user.Roles)
            claims.Add(new Claim(ClaimTypes.Role, role));

        var credentials = new SigningCredentials(
            new SymmetricSecurityKey(Encoding.UTF8.GetBytes(key)),
            SecurityAlgorithms.HmacSha256);

        var token = new JwtSecurityToken(
            issuer: issuer,
            audience: audience,
            claims: claims,
            expires: DateTime.UtcNow.AddHours(hours),
            signingCredentials: credentials);

        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}
