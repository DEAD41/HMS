using HealthcareERP.Modules.Procurement.Services;
using Microsoft.AspNetCore.Mvc;

namespace HealthcareERP.Api.Controllers;

[ApiController]
[Route("api/prc")]
public sealed class ProcurementController(
    ProcurementService procurementService,
    VendorPerformanceService vendorPerformanceService) : ControllerBase
{
    public sealed record CreateVendorRequest(Guid FacilityId, string Code, string Name);
    public sealed record IssuePoRequest(
        Guid FacilityId,
        Guid VendorId,
        Guid? RequisitionId,
        Guid? ItemId,
        decimal Quantity,
        decimal UnitPrice,
        string Currency);
    public sealed record PublishScorecardRequest(Guid FacilityId, string Period);

    [HttpGet("vendors")]
    public async Task<IActionResult> ListVendors([FromQuery] Guid facilityId, CancellationToken cancellationToken) =>
        Ok(await procurementService.ListVendorsAsync(facilityId, cancellationToken));

    [HttpPost("vendors")]
    public async Task<IActionResult> CreateVendor([FromBody] CreateVendorRequest request, CancellationToken cancellationToken)
    {
        var result = await procurementService.CreateVendorAsync(request.FacilityId, request.Code, request.Name, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpGet("requisitions")]
    public async Task<IActionResult> ListRequisitions([FromQuery] Guid facilityId, CancellationToken cancellationToken) =>
        Ok(await procurementService.ListRequisitionsAsync(facilityId, cancellationToken));

    [HttpPost("purchase-orders")]
    public async Task<IActionResult> IssuePurchaseOrder([FromBody] IssuePoRequest request, CancellationToken cancellationToken)
    {
        var result = await procurementService.IssuePurchaseOrderAsync(
            request.FacilityId,
            request.VendorId,
            request.RequisitionId,
            request.ItemId,
            request.Quantity,
            request.UnitPrice,
            request.Currency,
            cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpGet("vendors/{id:guid}/scorecard")]
    public async Task<IActionResult> GetScorecard(Guid id, CancellationToken cancellationToken)
    {
        var card = await vendorPerformanceService.GetForVendorAsync(id, cancellationToken);
        return card is null ? NotFound(new { error = "Scorecard not found. Publish one first." }) : Ok(card);
    }

    [HttpPost("vendors/{id:guid}/scorecards/publish")]
    public async Task<IActionResult> PublishScorecard(Guid id, [FromBody] PublishScorecardRequest request, CancellationToken cancellationToken)
    {
        var result = await vendorPerformanceService.PublishAsync(request.FacilityId, id, request.Period, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpGet("scorecards")]
    public async Task<IActionResult> ListScorecards([FromQuery] Guid facilityId, CancellationToken cancellationToken) =>
        Ok(await vendorPerformanceService.ListAsync(facilityId, cancellationToken));
}
