using HealthcareERP.Modules.Hms.Services;
using Microsoft.AspNetCore.Mvc;

namespace HealthcareERP.Api.Controllers;

[ApiController]
[Route("api/hms/ipd")]
public sealed class IpdController(IpdService ipdService, NursingService nursingService) : ControllerBase
{
    public sealed record CreateBedRequest(Guid FacilityId, string Code, string Ward, string BedClass);
    public sealed record AdmitRequest(
        Guid FacilityId,
        Guid PatientId,
        Guid AttendingClinicianId,
        Guid BedId,
        string AdmittingDiagnosis,
        decimal DailyBedCharge,
        string Currency);
    public sealed record CreateCarePlanRequest(Guid FacilityId, Guid AdmissionId, string Summary, string Goals);
    public sealed record RecordMarRequest(
        Guid FacilityId,
        Guid AdmissionId,
        Guid MedicationDispenseId,
        Guid NurseEmployeeId,
        string DoseInstanceId,
        string Action,
        string? Notes);

    [HttpGet("beds")]
    public async Task<IActionResult> ListBeds([FromQuery] Guid facilityId, CancellationToken cancellationToken) =>
        Ok(await ipdService.ListBedsAsync(facilityId, cancellationToken));

    [HttpPost("beds")]
    public async Task<IActionResult> CreateBed([FromBody] CreateBedRequest request, CancellationToken cancellationToken)
    {
        var result = await ipdService.CreateBedAsync(request.FacilityId, request.Code, request.Ward, request.BedClass, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpGet("admissions")]
    public async Task<IActionResult> ListAdmissions([FromQuery] Guid facilityId, CancellationToken cancellationToken) =>
        Ok(await ipdService.ListAdmissionsAsync(facilityId, cancellationToken));

    [HttpPost("admissions")]
    public async Task<IActionResult> Admit([FromBody] AdmitRequest request, CancellationToken cancellationToken)
    {
        var result = await ipdService.AdmitAsync(
            request.FacilityId, request.PatientId, request.AttendingClinicianId, request.BedId,
            request.AdmittingDiagnosis, request.DailyBedCharge, request.Currency, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpGet("care-plans")]
    public async Task<IActionResult> ListCarePlans([FromQuery] Guid admissionId, CancellationToken cancellationToken) =>
        Ok(await nursingService.ListCarePlansAsync(admissionId, cancellationToken));

    [HttpPost("care-plans")]
    public async Task<IActionResult> CreateCarePlan([FromBody] CreateCarePlanRequest request, CancellationToken cancellationToken)
    {
        var result = await nursingService.CreateCarePlanAsync(
            request.FacilityId, request.AdmissionId, request.Summary, request.Goals, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpGet("mar")]
    public async Task<IActionResult> ListMar([FromQuery] Guid admissionId, CancellationToken cancellationToken) =>
        Ok(await nursingService.ListMarAsync(admissionId, cancellationToken));

    [HttpPost("mar")]
    public async Task<IActionResult> RecordMar([FromBody] RecordMarRequest request, CancellationToken cancellationToken)
    {
        var result = await nursingService.RecordMarAsync(
            request.FacilityId, request.AdmissionId, request.MedicationDispenseId, request.NurseEmployeeId,
            request.DoseInstanceId, request.Action, request.Notes, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }
}
