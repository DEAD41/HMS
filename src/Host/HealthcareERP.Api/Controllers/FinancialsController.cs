using HealthcareERP.Modules.Financials.Services;
using Microsoft.AspNetCore.Mvc;

namespace HealthcareERP.Api.Controllers;

[ApiController]
[Route("api/fin")]
public sealed class FinancialsController(
    LedgerService ledgerService,
    ReceivableService receivableService,
    AccountsPayableService accountsPayableService,
    BudgetService budgetService,
    MisService misService) : ControllerBase
{
    public sealed record CreateAccountRequest(Guid FacilityId, string Code, string Name, string Type);
    public sealed record CreateCostCenterRequest(Guid FacilityId, string Code, string Name);
    public sealed record CaptureInvoiceRequest(
        Guid FacilityId,
        Guid VendorId,
        string InvoiceNumber,
        decimal Amount,
        string Currency,
        Guid? PurchaseOrderId,
        Guid? GoodsReceiptId);
    public sealed record CreateBudgetRequest(
        Guid FacilityId,
        Guid CostCenterId,
        string Period,
        string AccountCode,
        decimal Amount);
    public sealed record RecordActualRequest(decimal Amount);

    [HttpGet("accounts")]
    public async Task<IActionResult> ListAccounts([FromQuery] Guid facilityId, CancellationToken cancellationToken) =>
        Ok(await ledgerService.ListAccountsAsync(facilityId, cancellationToken));

    [HttpPost("accounts")]
    public async Task<IActionResult> CreateAccount([FromBody] CreateAccountRequest request, CancellationToken cancellationToken)
    {
        var result = await ledgerService.CreateAccountAsync(request.FacilityId, request.Code, request.Name, request.Type, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("cost-centers")]
    public async Task<IActionResult> CreateCostCenter([FromBody] CreateCostCenterRequest request, CancellationToken cancellationToken)
    {
        var result = await ledgerService.CreateCostCenterAsync(request.FacilityId, request.Code, request.Name, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpGet("receivables")]
    public async Task<IActionResult> ListReceivables([FromQuery] Guid facilityId, CancellationToken cancellationToken) =>
        Ok(await receivableService.ListAsync(facilityId, cancellationToken));

    [HttpGet("payroll-expenses")]
    public async Task<IActionResult> ListPayrollExpenses([FromQuery] Guid facilityId, CancellationToken cancellationToken) =>
        Ok(await ledgerService.ListPayrollExpensesAsync(facilityId, cancellationToken));

    [HttpPost("ap/invoices")]
    public async Task<IActionResult> CaptureInvoice([FromBody] CaptureInvoiceRequest request, CancellationToken cancellationToken)
    {
        var result = await accountsPayableService.CaptureInvoiceAsync(
            request.FacilityId,
            request.VendorId,
            request.InvoiceNumber,
            request.Amount,
            request.Currency,
            request.PurchaseOrderId,
            request.GoodsReceiptId,
            cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("ap/invoices/{id:guid}/match")]
    public async Task<IActionResult> MatchInvoice(Guid id, CancellationToken cancellationToken)
    {
        var result = await accountsPayableService.MatchAsync(id, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpGet("budgets")]
    public async Task<IActionResult> ListBudgets([FromQuery] Guid facilityId, [FromQuery] string? period, CancellationToken cancellationToken) =>
        Ok(await budgetService.ListAsync(facilityId, period, cancellationToken));

    [HttpPost("budgets")]
    public async Task<IActionResult> CreateBudget([FromBody] CreateBudgetRequest request, CancellationToken cancellationToken)
    {
        var result = await budgetService.CreateAsync(
            request.FacilityId, request.CostCenterId, request.Period, request.AccountCode, request.Amount, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("budgets/{id:guid}/activate")]
    public async Task<IActionResult> ActivateBudget(Guid id, CancellationToken cancellationToken)
    {
        var result = await budgetService.ActivateAsync(id, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("budgets/{id:guid}/actuals")]
    public async Task<IActionResult> RecordActual(Guid id, [FromBody] RecordActualRequest request, CancellationToken cancellationToken)
    {
        var result = await budgetService.RecordActualAsync(id, request.Amount, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpGet("budgets/variance")]
    public async Task<IActionResult> BudgetVariance([FromQuery] Guid facilityId, [FromQuery] string? period, CancellationToken cancellationToken) =>
        Ok(await budgetService.VarianceAsync(facilityId, period, cancellationToken));

    [HttpGet("mis/dashboard")]
    public async Task<IActionResult> MisDashboard([FromQuery] Guid facilityId, CancellationToken cancellationToken) =>
        Ok(await misService.GetDashboardAsync(facilityId, cancellationToken));
}
