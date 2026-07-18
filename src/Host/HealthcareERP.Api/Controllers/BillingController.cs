using HealthcareERP.Modules.Hms.Services;
using Microsoft.AspNetCore.Mvc;

namespace HealthcareERP.Api.Controllers;

[ApiController]
[Route("api/hms/billing")]
public sealed class BillingController(BillingService billingService) : ControllerBase
{
    [HttpGet("patients/{patientId:guid}/charges")]
    public async Task<IActionResult> ListCharges(Guid patientId, CancellationToken cancellationToken) =>
        Ok(await billingService.ListForPatientAsync(patientId, cancellationToken));
}
