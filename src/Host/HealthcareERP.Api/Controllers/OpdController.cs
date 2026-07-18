using HealthcareERP.Modules.Hms.Services;
using Microsoft.AspNetCore.Mvc;

namespace HealthcareERP.Api.Controllers;

[ApiController]
[Route("api/hms/opd/encounters")]
public sealed class OpdController(OpdService opdService) : ControllerBase
{
    public sealed record OpenEncounterRequest(Guid FacilityId, Guid PatientId, Guid ClinicianEmployeeId, Guid? AppointmentId, string? ChiefComplaint);
    public sealed record CloseEncounterRequest(string Disposition, decimal ConsultationFee, string Currency);

    [HttpPost]
    public async Task<IActionResult> Open([FromBody] OpenEncounterRequest request, CancellationToken cancellationToken)
    {
        var result = await opdService.OpenAsync(request.FacilityId, request.PatientId, request.ClinicianEmployeeId, request.AppointmentId, request.ChiefComplaint, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("{id:guid}/close")]
    public async Task<IActionResult> Close(Guid id, [FromBody] CloseEncounterRequest request, CancellationToken cancellationToken)
    {
        var result = await opdService.CloseAsync(id, request.Disposition, request.ConsultationFee, request.Currency, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }
}
