using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Hms.Domain;

public sealed class MedicationDispense : AggregateRoot
{
    private MedicationDispense() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid? EncounterId { get; private set; }
    public Guid ItemId { get; private set; }
    public Guid StoreId { get; private set; }
    public string MedicationName { get; private set; } = string.Empty;
    public decimal Quantity { get; private set; }
    public string Status { get; private set; } = "Posted";

    public static Result<MedicationDispense> Post(
        Guid facilityId,
        Guid patientId,
        Guid itemId,
        Guid storeId,
        string medicationName,
        decimal quantity,
        Guid? encounterId)
    {
        if (quantity <= 0) return Result.Failure<MedicationDispense>("Quantity must be positive.");
        if (itemId == Guid.Empty || storeId == Guid.Empty)
            return Result.Failure<MedicationDispense>("Item and store are required.");
        if (string.IsNullOrWhiteSpace(medicationName))
            return Result.Failure<MedicationDispense>("Medication name is required.");

        return Result.Success(new MedicationDispense
        {
            FacilityId = facilityId,
            PatientId = patientId,
            EncounterId = encounterId,
            ItemId = itemId,
            StoreId = storeId,
            MedicationName = medicationName.Trim(),
            Quantity = quantity,
            Status = "Posted"
        });
    }
}
