using HealthcareERP.Modules.Hris.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace HealthcareERP.Api.Controllers;

[ApiController]
[Route("api/hris")]
public sealed class HrisController(
    EmployeeService employeeService,
    CredentialService credentialService,
    RosterService rosterService,
    LeaveService leaveService,
    PayrollService payrollService,
    EssService essService) : ControllerBase
{
    public sealed record CreateEmployeeRequest(
        Guid FacilityId,
        string EmployeeCode,
        string FirstName,
        string LastName,
        string Department,
        string JobTitle,
        DateOnly JoinDate,
        Guid? ManagerEmployeeId,
        Guid? CostCenterRef);

    public sealed record AddCredentialRequest(
        Guid FacilityId,
        Guid EmployeeId,
        string Type,
        string Number,
        string Specialty,
        DateOnly IssueDate,
        DateOnly ExpiryDate);

    public sealed record PublishRosterRequest(
        Guid FacilityId,
        Guid EmployeeId,
        string Department,
        string ShiftCode,
        DateOnly DutyDate);

    public sealed record SubmitLeaveRequest(
        Guid FacilityId,
        Guid EmployeeId,
        string LeaveType,
        DateOnly StartDate,
        DateOnly EndDate,
        string? Reason);

    public sealed record CreatePayrollRequest(Guid FacilityId, string Period, decimal GrossAmount, decimal Deductions);
    public sealed record EssLeaveRequest(string LeaveType, DateOnly StartDate, DateOnly EndDate, string? Reason);

    [HttpGet("employees")]
    public async Task<IActionResult> ListEmployees([FromQuery] Guid facilityId, CancellationToken cancellationToken) =>
        Ok(await employeeService.ListAsync(facilityId, cancellationToken));

    [Authorize]
    [HttpGet("ess/me")]
    public async Task<IActionResult> EssMe(CancellationToken cancellationToken)
    {
        var result = await essService.GetMeAsync(cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [Authorize]
    [HttpPost("ess/leave")]
    public async Task<IActionResult> EssLeave([FromBody] EssLeaveRequest request, CancellationToken cancellationToken)
    {
        var result = await essService.SubmitLeaveAsync(request.LeaveType, request.StartDate, request.EndDate, request.Reason, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("employees")]
    public async Task<IActionResult> CreateEmployee([FromBody] CreateEmployeeRequest request, CancellationToken cancellationToken)
    {
        var result = await employeeService.CreateAsync(
            request.FacilityId, request.EmployeeCode, request.FirstName, request.LastName,
            request.Department, request.JobTitle, request.JoinDate, request.ManagerEmployeeId, request.CostCenterRef, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("employees/{id:guid}/activate")]
    public async Task<IActionResult> ActivateEmployee(Guid id, CancellationToken cancellationToken)
    {
        var result = await employeeService.ActivateAsync(id, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("employees/{id:guid}/exit")]
    public async Task<IActionResult> ExitEmployee(Guid id, CancellationToken cancellationToken)
    {
        var result = await employeeService.ExitAsync(id, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpGet("credentials")]
    public async Task<IActionResult> ListCredentials([FromQuery] Guid employeeId, CancellationToken cancellationToken) =>
        Ok(await credentialService.ListForEmployeeAsync(employeeId, cancellationToken));

    [HttpPost("credentials")]
    public async Task<IActionResult> AddCredential([FromBody] AddCredentialRequest request, CancellationToken cancellationToken)
    {
        var result = await credentialService.AddAsync(
            request.FacilityId, request.EmployeeId, request.Type, request.Number, request.Specialty,
            request.IssueDate, request.ExpiryDate, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("credentials/{id:guid}/verify")]
    public async Task<IActionResult> VerifyCredential(Guid id, CancellationToken cancellationToken)
    {
        var result = await credentialService.VerifyAsync(id, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpGet("roster")]
    public async Task<IActionResult> ListRoster([FromQuery] Guid facilityId, [FromQuery] DateOnly? dutyDate, CancellationToken cancellationToken) =>
        Ok(await rosterService.ListAsync(facilityId, dutyDate, cancellationToken));

    [HttpPost("roster")]
    public async Task<IActionResult> PublishRoster([FromBody] PublishRosterRequest request, CancellationToken cancellationToken)
    {
        var result = await rosterService.PublishAsync(
            request.FacilityId, request.EmployeeId, request.Department, request.ShiftCode, request.DutyDate, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpGet("leave")]
    public async Task<IActionResult> ListLeave([FromQuery] Guid facilityId, CancellationToken cancellationToken) =>
        Ok(await leaveService.ListAsync(facilityId, cancellationToken));

    [HttpPost("leave")]
    public async Task<IActionResult> SubmitLeave([FromBody] SubmitLeaveRequest request, CancellationToken cancellationToken)
    {
        var result = await leaveService.SubmitAsync(
            request.FacilityId, request.EmployeeId, request.LeaveType, request.StartDate, request.EndDate, request.Reason, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("leave/{id:guid}/approve")]
    public async Task<IActionResult> ApproveLeave(Guid id, CancellationToken cancellationToken)
    {
        var result = await leaveService.ApproveAsync(id, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpGet("payroll")]
    public async Task<IActionResult> ListPayroll([FromQuery] Guid facilityId, CancellationToken cancellationToken) =>
        Ok(await payrollService.ListAsync(facilityId, cancellationToken));

    [HttpPost("payroll")]
    public async Task<IActionResult> CreatePayroll([FromBody] CreatePayrollRequest request, CancellationToken cancellationToken)
    {
        var result = await payrollService.CreateAsync(request.FacilityId, request.Period, request.GrossAmount, request.Deductions, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }

    [HttpPost("payroll/{id:guid}/post")]
    public async Task<IActionResult> PostPayroll(Guid id, CancellationToken cancellationToken)
    {
        var result = await payrollService.PostAsync(id, cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(new { error = result.Error });
    }
}
