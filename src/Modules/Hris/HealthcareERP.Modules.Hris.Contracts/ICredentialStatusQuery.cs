namespace HealthcareERP.Modules.Hris.Contracts;

public interface ICredentialStatusQuery
{
    Task<bool> IsClinicianSchedulableAsync(Guid employeeId, Guid facilityId, CancellationToken cancellationToken = default);
    Task<bool> IsNurseCapableAsync(Guid employeeId, Guid facilityId, CancellationToken cancellationToken = default);
}
