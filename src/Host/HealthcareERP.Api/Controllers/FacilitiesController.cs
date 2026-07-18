using HealthcareERP.Modules.Foundation.Services;
using Microsoft.AspNetCore.Mvc;

namespace HealthcareERP.Api.Controllers;

[ApiController]
[Route("api/fnd/facilities")]
public sealed class FacilitiesController(FacilityService facilityService) : ControllerBase
{
    public sealed record CreateFacilityRequest(string Code, string Name, string Timezone, string Currency);
    public sealed record CreateOrgUnitRequest(string Code, string Name, string Type, Guid? ParentId, Guid? CostCenterRef);

    [HttpGet]
    public async Task<IActionResult> List(CancellationToken cancellationToken) =>
        Ok(await facilityService.ListAsync(cancellationToken));

    [HttpPost]
    public async Task<IActionResult> Create([FromBody] CreateFacilityRequest request, CancellationToken cancellationToken)
    {
        var result = await facilityService.CreateAsync(request.Code, request.Name, request.Timezone, request.Currency, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpGet("{facilityId:guid}/org-units")]
    public async Task<IActionResult> ListOrgUnits(Guid facilityId, CancellationToken cancellationToken) =>
        Ok(await facilityService.ListOrgUnitsAsync(facilityId, cancellationToken));

    [HttpPost("{facilityId:guid}/org-units")]
    public async Task<IActionResult> CreateOrgUnit(Guid facilityId, [FromBody] CreateOrgUnitRequest request, CancellationToken cancellationToken)
    {
        var result = await facilityService.CreateOrgUnitAsync(facilityId, request.Code, request.Name, request.Type, request.ParentId, request.CostCenterRef, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }
}
