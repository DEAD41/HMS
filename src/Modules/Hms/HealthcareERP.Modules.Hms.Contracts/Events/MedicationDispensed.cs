namespace HealthcareERP.Modules.Hms.Contracts.Events;

public sealed record MedicationDispensed(
    Guid DispenseId,
    Guid FacilityId,
    Guid PatientId,
    Guid ItemId,
    Guid StoreId,
    decimal Quantity,
    string MedicationName);
