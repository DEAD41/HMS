using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Procurement.Domain;

public sealed class VendorScorecard : AggregateRoot
{
    private VendorScorecard() { }

    public Guid FacilityId { get; private set; }
    public Guid VendorId { get; private set; }
    public string Period { get; private set; } = string.Empty;
    public int OrdersCount { get; private set; }
    public decimal TotalSpend { get; private set; }
    public decimal OnTimePercent { get; private set; }
    public decimal QualityPercent { get; private set; }
    public decimal OverallScore { get; private set; }
    public string ComplianceStatus { get; private set; } = "Compliant";
    public string Status { get; private set; } = "Published";

    public static Result<VendorScorecard> Publish(
        Guid facilityId,
        Guid vendorId,
        string period,
        int ordersCount,
        decimal totalSpend,
        decimal onTimePercent,
        decimal qualityPercent)
    {
        if (vendorId == Guid.Empty) return Result.Failure<VendorScorecard>("Vendor is required.");
        if (string.IsNullOrWhiteSpace(period)) return Result.Failure<VendorScorecard>("Period is required.");

        var overall = Math.Round((onTimePercent + qualityPercent) / 2m, 2);
        var compliance = overall >= 80 ? "Compliant" : overall >= 60 ? "Warning" : "NonCompliant";

        return Result.Success(new VendorScorecard
        {
            FacilityId = facilityId,
            VendorId = vendorId,
            Period = period.Trim(),
            OrdersCount = ordersCount,
            TotalSpend = totalSpend,
            OnTimePercent = onTimePercent,
            QualityPercent = qualityPercent,
            OverallScore = overall,
            ComplianceStatus = compliance,
            Status = "Published"
        });
    }
}
