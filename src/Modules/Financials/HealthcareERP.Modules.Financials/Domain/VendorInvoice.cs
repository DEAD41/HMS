using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Financials.Domain;

public sealed class VendorInvoice : AggregateRoot
{
    private VendorInvoice() { }

    public Guid FacilityId { get; private set; }
    public Guid VendorId { get; private set; }
    public Guid? PurchaseOrderId { get; private set; }
    public Guid? GoodsReceiptId { get; private set; }
    public string InvoiceNumber { get; private set; } = string.Empty;
    public decimal Amount { get; private set; }
    public string Currency { get; private set; } = "USD";
    public string Status { get; private set; } = "Received";

    public static Result<VendorInvoice> Create(
        Guid facilityId,
        Guid vendorId,
        string invoiceNumber,
        decimal amount,
        string currency,
        Guid? purchaseOrderId,
        Guid? goodsReceiptId)
    {
        if (amount < 0) return Result.Failure<VendorInvoice>("Amount cannot be negative.");
        if (string.IsNullOrWhiteSpace(invoiceNumber)) return Result.Failure<VendorInvoice>("Invoice number is required.");

        return Result.Success(new VendorInvoice
        {
            FacilityId = facilityId,
            VendorId = vendorId,
            InvoiceNumber = invoiceNumber.Trim(),
            Amount = amount,
            Currency = currency.Trim().ToUpperInvariant(),
            PurchaseOrderId = purchaseOrderId,
            GoodsReceiptId = goodsReceiptId,
            Status = "Received"
        });
    }

    public Result Match()
    {
        if (PurchaseOrderId is null || GoodsReceiptId is null)
            return Result.Failure("PO and GRN are required for three-way match.");
        Status = "Matched";
        Touch();
        return Result.Success();
    }
}
