using Microsoft.AspNetCore.Mvc;

namespace HealthcareERP.Api.Controllers;

[ApiController]
[Route("api/health")]
public sealed class HealthController : ControllerBase
{
    [HttpGet]
    public IActionResult Get() => Ok(new
    {
        status = "Healthy",
        service = "HealthcareERP.Api",
        utc = DateTimeOffset.UtcNow
    });
}
