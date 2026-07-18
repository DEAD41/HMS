using HealthcareERP.Modules.Hms.Services;
using Microsoft.AspNetCore.Mvc;

namespace HealthcareERP.Api.Controllers;

[ApiController]
[Route("api/hms/patients")]
public sealed class PatientsController(PatientService patientService) : ControllerBase
{
    public sealed record RegisterPatientRequest(
        Guid FacilityId,
        string Mrn,
        string FirstName,
        string LastName,
        DateOnly? DateOfBirth,
        string? Phone,
        string? NationalId);

    [HttpGet]
    public async Task<IActionResult> Search([FromQuery] Guid facilityId, [FromQuery] string? query, CancellationToken cancellationToken) =>
        Ok(await patientService.SearchAsync(facilityId, query, cancellationToken));

    [HttpPost]
    public async Task<IActionResult> Register([FromBody] RegisterPatientRequest request, CancellationToken cancellationToken)
    {
        var result = await patientService.RegisterAsync(
            request.FacilityId, request.Mrn, request.FirstName, request.LastName,
            request.DateOfBirth, request.Phone, request.NationalId, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }
}
