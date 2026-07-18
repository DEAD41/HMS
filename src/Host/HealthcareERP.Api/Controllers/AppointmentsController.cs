using HealthcareERP.Modules.Hms.Services;
using Microsoft.AspNetCore.Mvc;

namespace HealthcareERP.Api.Controllers;

[ApiController]
[Route("api/hms/appointments")]
public sealed class AppointmentsController(AppointmentService appointmentService) : ControllerBase
{
    public sealed record ScheduleRequest(
        Guid FacilityId,
        Guid PatientId,
        Guid ClinicianEmployeeId,
        DateTimeOffset StartsAt,
        DateTimeOffset EndsAt,
        Guid? ClinicOrgUnitId,
        string? Reason);

    [HttpGet]
    public async Task<IActionResult> List([FromQuery] Guid facilityId, [FromQuery] DateOnly date, CancellationToken cancellationToken) =>
        Ok(await appointmentService.ListAsync(facilityId, date, cancellationToken));

    [HttpPost]
    public async Task<IActionResult> Schedule([FromBody] ScheduleRequest request, CancellationToken cancellationToken)
    {
        var result = await appointmentService.ScheduleAsync(
            request.FacilityId, request.PatientId, request.ClinicianEmployeeId,
            request.StartsAt, request.EndsAt, request.ClinicOrgUnitId, request.Reason, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("{id:guid}/check-in")]
    public async Task<IActionResult> CheckIn(Guid id, CancellationToken cancellationToken)
    {
        var result = await appointmentService.CheckInAsync(id, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }
}
