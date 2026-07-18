using HealthcareERP.Modules.Hms.Services;
using Microsoft.AspNetCore.Mvc;

namespace HealthcareERP.Api.Controllers;

[ApiController]
[Route("api/hms")]
public sealed class ClinicalOpsController(
    EmergencyService emergencyService,
    OtService otService,
    LisService lisService,
    RisService risService,
    PharmacyService pharmacyService,
    DischargeService dischargeService) : ControllerBase
{
    public sealed record OpenErRequest(Guid FacilityId, Guid? PatientId, string? TemporaryId);
    public sealed record TriageRequest(string Category);
    public sealed record DisposeErRequest(string Disposition);
    public sealed record ScheduleOtRequest(Guid FacilityId, Guid PatientId, Guid SurgeonEmployeeId, string TheatreCode, string ProcedureName, DateTimeOffset ScheduledAt);
    public sealed record CompleteOtRequest(decimal ProcedureFee, string Currency);
    public sealed record AcceptLabRequest(Guid FacilityId, Guid PatientId, string TestCode, string TestName, Guid? EncounterId, decimal ChargeAmount, string Currency);
    public sealed record FinalizeLabRequest(string ResultValue, bool IsCritical);
    public sealed record AdapterImportRequest(string? RawPayload);
    public sealed record CollectSampleRequest(string? SampleId);
    public sealed record AcceptRadRequest(Guid FacilityId, Guid PatientId, string Modality, string StudyName, Guid? EncounterId, decimal ChargeAmount, string Currency);
    public sealed record SignRadRequest(string ReportText);
    public sealed record DispenseRequest(Guid FacilityId, Guid PatientId, Guid ItemId, Guid StoreId, string MedicationName, decimal Quantity, decimal UnitPrice, string Currency, Guid? EncounterId);
    public sealed record DischargeRequest(Guid FacilityId, Guid AdmissionId, string Summary, bool ScheduleFollowUp, Guid? ClinicianEmployeeId, DateTimeOffset? FollowUpAt);

    [HttpPost("er/encounters")]
    public async Task<IActionResult> OpenEr([FromBody] OpenErRequest request, CancellationToken cancellationToken)
    {
        var result = await emergencyService.OpenAsync(request.FacilityId, request.PatientId, request.TemporaryId, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("er/encounters/{id:guid}/triage")]
    public async Task<IActionResult> Triage(Guid id, [FromBody] TriageRequest request, CancellationToken cancellationToken)
    {
        var result = await emergencyService.TriageAsync(id, request.Category, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("er/encounters/{id:guid}/dispose")]
    public async Task<IActionResult> DisposeEr(Guid id, [FromBody] DisposeErRequest request, CancellationToken cancellationToken)
    {
        var result = await emergencyService.DisposeAsync(id, request.Disposition, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("ot/cases")]
    public async Task<IActionResult> ScheduleOt([FromBody] ScheduleOtRequest request, CancellationToken cancellationToken)
    {
        var result = await otService.ScheduleAsync(
            request.FacilityId, request.PatientId, request.SurgeonEmployeeId, request.TheatreCode,
            request.ProcedureName, request.ScheduledAt, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("ot/cases/{id:guid}/checklist")]
    public async Task<IActionResult> CompleteChecklist(Guid id, CancellationToken cancellationToken)
    {
        var result = await otService.CompleteChecklistAsync(id, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("ot/cases/{id:guid}/complete")]
    public async Task<IActionResult> CompleteOt(Guid id, [FromBody] CompleteOtRequest request, CancellationToken cancellationToken)
    {
        var result = await otService.CompleteAsync(id, request.ProcedureFee, request.Currency, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("lis/orders")]
    public async Task<IActionResult> AcceptLab([FromBody] AcceptLabRequest request, CancellationToken cancellationToken)
    {
        var result = await lisService.AcceptAsync(
            request.FacilityId, request.PatientId, request.TestCode, request.TestName,
            request.EncounterId, request.ChargeAmount, request.Currency, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("lis/orders/{id:guid}/samples")]
    public async Task<IActionResult> CollectSample(Guid id, [FromBody] CollectSampleRequest request, CancellationToken cancellationToken)
    {
        var result = await lisService.CollectSampleAsync(id, request.SampleId, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("lis/adapters/import/{id:guid}")]
    public async Task<IActionResult> ImportLab(Guid id, [FromBody] AdapterImportRequest request, CancellationToken cancellationToken)
    {
        var result = await lisService.ImportFromAdapterAsync(id, request.RawPayload, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("lis/orders/{id:guid}/finalize")]
    public async Task<IActionResult> FinalizeLab(Guid id, [FromBody] FinalizeLabRequest request, CancellationToken cancellationToken)
    {
        var result = await lisService.FinalizeAsync(id, request.ResultValue, request.IsCritical, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpGet("lis/orders")]
    public async Task<IActionResult> ListLab([FromQuery] Guid facilityId, CancellationToken cancellationToken) =>
        Ok(await lisService.ListAsync(facilityId, cancellationToken));

    [HttpPost("ris/orders")]
    public async Task<IActionResult> AcceptRad([FromBody] AcceptRadRequest request, CancellationToken cancellationToken)
    {
        var result = await risService.AcceptAsync(
            request.FacilityId, request.PatientId, request.Modality, request.StudyName,
            request.EncounterId, request.ChargeAmount, request.Currency, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("ris/adapters/study-status/{id:guid}")]
    public async Task<IActionResult> AcquireStudy(Guid id, CancellationToken cancellationToken)
    {
        var result = await risService.AcquireFromAdapterAsync(id, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("ris/orders/{id:guid}/sign")]
    public async Task<IActionResult> SignRad(Guid id, [FromBody] SignRadRequest request, CancellationToken cancellationToken)
    {
        var result = await risService.SignReportAsync(id, request.ReportText, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("pharmacy/dispense")]
    public async Task<IActionResult> Dispense([FromBody] DispenseRequest request, CancellationToken cancellationToken)
    {
        var result = await pharmacyService.DispenseAsync(
            request.FacilityId, request.PatientId, request.ItemId, request.StoreId, request.MedicationName,
            request.Quantity, request.UnitPrice, request.Currency, request.EncounterId, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("discharge")]
    public async Task<IActionResult> Discharge([FromBody] DischargeRequest request, CancellationToken cancellationToken)
    {
        var result = await dischargeService.CompleteAsync(
            request.FacilityId, request.AdmissionId, request.Summary, request.ScheduleFollowUp,
            request.ClinicianEmployeeId, request.FollowUpAt, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }
}
