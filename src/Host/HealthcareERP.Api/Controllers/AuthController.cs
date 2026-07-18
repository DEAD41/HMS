using HealthcareERP.Api.Services;
using HealthcareERP.Modules.Foundation.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace HealthcareERP.Api.Controllers;

[ApiController]
[Route("api/fnd/auth")]
public sealed class AuthController(AuthService authService, JwtTokenService jwtTokenService) : ControllerBase
{
    public sealed record LoginRequest(string UserName, string Password);
    public sealed record LinkEmployeeRequest(Guid EmployeeId);

    [AllowAnonymous]
    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] LoginRequest request, CancellationToken cancellationToken)
    {
        var result = await authService.LoginAsync(request.UserName, request.Password, cancellationToken);
        if (result.IsFailure) return Unauthorized(new { error = result.Error });

        var user = result.Value!;
        var token = jwtTokenService.CreateToken(user);
        return Ok(new
        {
            accessToken = token,
            tokenType = "Bearer",
            user = new
            {
                user.Id,
                user.UserName,
                user.DisplayName,
                Roles = user.Roles,
                user.EmployeeId,
                user.DefaultFacilityId
            }
        });
    }

    [Authorize]
    [HttpGet("me")]
    public async Task<IActionResult> Me(CancellationToken cancellationToken)
    {
        var userId = User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value;
        if (!Guid.TryParse(userId, out var id)) return Unauthorized();
        var user = await authService.GetByIdAsync(id, cancellationToken);
        return user is null ? NotFound() : Ok(new
        {
            user.Id,
            user.UserName,
            user.DisplayName,
            Roles = user.Roles,
            user.EmployeeId,
            user.DefaultFacilityId,
            user.Status
        });
    }

    [Authorize(Roles = "Admin")]
    [HttpGet("users")]
    public async Task<IActionResult> ListUsers(CancellationToken cancellationToken) =>
        Ok((await authService.ListAsync(cancellationToken)).Select(u => new
        {
            u.Id,
            u.UserName,
            u.DisplayName,
            Roles = u.Roles,
            u.EmployeeId,
            u.DefaultFacilityId,
            u.Status
        }));

    [Authorize(Roles = "Admin,Hr")]
    [HttpPost("users/{id:guid}/link-employee")]
    public async Task<IActionResult> LinkEmployee(Guid id, [FromBody] LinkEmployeeRequest request, CancellationToken cancellationToken)
    {
        var result = await authService.LinkEmployeeAsync(id, request.EmployeeId, cancellationToken);
        if (result.IsFailure) return BadRequest(new { error = result.Error });
        var token = jwtTokenService.CreateToken(result.Value!);
        return Ok(new
        {
            user = result.Value,
            accessToken = token,
            note = "Use the new accessToken so employee_id claim is present."
        });
    }

    [AllowAnonymous]
    [HttpGet("demo-users")]
    public IActionResult DemoUsers() => Ok(new[]
    {
        new { userName = "admin", password = "Admin@123", roles = new[] { "Admin", "Finance", "Hr", "Clinician", "Employee" } },
        new { userName = "doctor", password = "Doctor@123", roles = new[] { "Clinician", "Employee" } },
        new { userName = "hr", password = "Hr@123", roles = new[] { "Hr", "Employee" } },
        new { userName = "finance", password = "Finance@123", roles = new[] { "Finance", "Employee" } },
        new { userName = "employee", password = "Employee@123", roles = new[] { "Employee" } },
    });
}
