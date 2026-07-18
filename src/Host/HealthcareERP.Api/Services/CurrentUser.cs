using System.Security.Claims;
using HealthcareERP.BuildingBlocks.Application.Abstractions;

namespace HealthcareERP.Api.Services;

public sealed class CurrentUser(IHttpContextAccessor accessor) : ICurrentUser
{
    public Guid? UserId => Guid.TryParse(accessor.HttpContext?.User.FindFirstValue(ClaimTypes.NameIdentifier), out var id) ? id : null;
    public string? UserName => accessor.HttpContext?.User.Identity?.Name
        ?? accessor.HttpContext?.User.FindFirstValue(ClaimTypes.Name)
        ?? accessor.HttpContext?.User.FindFirstValue("name");
    public Guid? FacilityId =>
        Guid.TryParse(accessor.HttpContext?.User.FindFirstValue("facility_id"), out var fromClaim) ? fromClaim
        : Guid.TryParse(accessor.HttpContext?.Request.Headers["X-Facility-Id"], out var fromHeader) ? fromHeader
        : null;
    public Guid? EmployeeId =>
        Guid.TryParse(accessor.HttpContext?.User.FindFirstValue("employee_id"), out var id) ? id : null;
    public bool IsAuthenticated => accessor.HttpContext?.User?.Identity?.IsAuthenticated == true;
    public IReadOnlyList<string> Roles =>
        accessor.HttpContext?.User?.FindAll(ClaimTypes.Role).Select(c => c.Value).ToArray() ?? [];
}
