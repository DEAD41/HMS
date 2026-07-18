using HealthcareERP.Modules.Inventory.Services;
using Microsoft.AspNetCore.Mvc;

namespace HealthcareERP.Api.Controllers;

[ApiController]
[Route("api/inv")]
public sealed class InventoryController(InventoryService inventoryService) : ControllerBase
{
    public sealed record CreateItemRequest(Guid FacilityId, string Sku, string Name, string UnitOfMeasure, bool BatchControlled, decimal ReorderLevel);
    public sealed record CreateStoreRequest(Guid FacilityId, string Code, string Name);
    public sealed record StockReceiveRequest(
        Guid FacilityId,
        Guid StoreId,
        Guid ItemId,
        decimal Quantity,
        string? BatchNumber,
        DateOnly? ExpiryDate);
    public sealed record StockIssueRequest(Guid FacilityId, Guid StoreId, Guid ItemId, decimal Quantity);

    [HttpGet("items")]
    public async Task<IActionResult> ListItems([FromQuery] Guid facilityId, CancellationToken cancellationToken) =>
        Ok(await inventoryService.ListItemsAsync(facilityId, cancellationToken));

    [HttpPost("items")]
    public async Task<IActionResult> CreateItem([FromBody] CreateItemRequest request, CancellationToken cancellationToken)
    {
        var result = await inventoryService.CreateItemAsync(
            request.FacilityId, request.Sku, request.Name, request.UnitOfMeasure, request.BatchControlled, request.ReorderLevel, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("stores")]
    public async Task<IActionResult> CreateStore([FromBody] CreateStoreRequest request, CancellationToken cancellationToken)
    {
        var result = await inventoryService.CreateStoreAsync(request.FacilityId, request.Code, request.Name, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpGet("batches")]
    public async Task<IActionResult> ListBatches(
        [FromQuery] Guid facilityId,
        [FromQuery] Guid? itemId,
        [FromQuery] Guid? storeId,
        CancellationToken cancellationToken) =>
        Ok(await inventoryService.ListBatchesAsync(facilityId, itemId, storeId, cancellationToken));

    [HttpPost("receipts")]
    public async Task<IActionResult> Receive([FromBody] StockReceiveRequest request, CancellationToken cancellationToken)
    {
        var result = await inventoryService.ReceiveAsync(
            request.FacilityId, request.StoreId, request.ItemId, request.Quantity,
            request.BatchNumber, request.ExpiryDate, cancellationToken);
        if (result.IsFailure) return BadRequest(new { error = result.Error });
        return Ok(new { balance = result.Value.Balance, batch = result.Value.Batch });
    }

    [HttpPost("issues")]
    public async Task<IActionResult> Issue([FromBody] StockIssueRequest request, CancellationToken cancellationToken)
    {
        var result = await inventoryService.IssueAsync(request.FacilityId, request.StoreId, request.ItemId, request.Quantity, cancellationToken);
        if (result.IsFailure) return BadRequest(new { error = result.Error });
        return Ok(new { balance = result.Value.Balance, allocations = result.Value.Allocations });
    }
}
