using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Foundation.Contracts.Events;
using HealthcareERP.Modules.Foundation.Domain;
using HealthcareERP.Modules.Foundation.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Foundation.Services;

public sealed class FacilityService(
    FoundationDbContext db,
    IIntegrationEventPublisher publisher,
    IAuditWriter auditWriter)
{
    public async Task<Result<Facility>> CreateAsync(string code, string name, string timezone, string currency, CancellationToken cancellationToken = default)
    {
        if (await db.Facilities.AnyAsync(x => x.Code == code.Trim().ToUpperInvariant(), cancellationToken))
            return Result.Failure<Facility>("Facility code already exists.");

        var create = Facility.Create(code, name, timezone, currency);
        if (create.IsFailure) return create;

        var facility = create.Value!;
        db.Facilities.Add(facility);

        var payload = new FacilityCreated(facility.Id, facility.Code, facility.Name, facility.Timezone, facility.Currency);
        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(),
            "FacilityCreated",
            "v1",
            DateTimeOffset.UtcNow,
            null,
            null,
            facility.Id,
            facility.Id.ToString(),
            JsonSerializer.Serialize(payload)), cancellationToken);

        await auditWriter.WriteAsync("FND", "Create", nameof(Facility), facility.Id, null, JsonSerializer.Serialize(payload), cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(facility);
    }

    public Task<List<Facility>> ListAsync(CancellationToken cancellationToken = default) =>
        db.Facilities.AsNoTracking().OrderBy(x => x.Code).ToListAsync(cancellationToken);

    public async Task<Result<OrgUnit>> CreateOrgUnitAsync(Guid facilityId, string code, string name, string type, Guid? parentId, Guid? costCenterRef, CancellationToken cancellationToken = default)
    {
        var facility = await db.Facilities.FirstOrDefaultAsync(x => x.Id == facilityId, cancellationToken);
        if (facility is null) return Result.Failure<OrgUnit>("Facility not found.");
        if (!string.Equals(facility.Status, "Active", StringComparison.OrdinalIgnoreCase))
            return Result.Failure<OrgUnit>("Facility is not active.");

        if (await db.OrgUnits.AnyAsync(x => x.FacilityId == facilityId && x.Code == code.Trim().ToUpperInvariant(), cancellationToken))
            return Result.Failure<OrgUnit>("Org unit code already exists in facility.");

        var create = OrgUnit.Create(facilityId, code, name, type, parentId, costCenterRef);
        if (create.IsFailure) return create;

        db.OrgUnits.Add(create.Value!);
        await auditWriter.WriteAsync("FND", "Create", nameof(OrgUnit), create.Value!.Id, null, JsonSerializer.Serialize(new { create.Value.Code, create.Value.Name, create.Value.Type }), cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public Task<List<OrgUnit>> ListOrgUnitsAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.OrgUnits.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderBy(x => x.Code).ToListAsync(cancellationToken);
}
