namespace HealthcareERP.BuildingBlocks.Application.Abstractions;

public interface ICurrentUser
{
    Guid? UserId { get; }
    string? UserName { get; }
    Guid? FacilityId { get; }
    Guid? EmployeeId { get; }
    bool IsAuthenticated { get; }
    IReadOnlyList<string> Roles { get; }
}
