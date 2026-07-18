using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Financials.Domain;
using HealthcareERP.Modules.Financials.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Financials.Services;

public sealed class AccountsPayableService(FinancialsDbContext db, IAuditWriter auditWriter)
{
    public async Task<Result<VendorInvoice>> CaptureInvoiceAsync(
        Guid facilityId,
        Guid vendorId,
        string invoiceNumber,
        decimal amount,
        string currency,
        Guid? purchaseOrderId,
        Guid? goodsReceiptId,
        CancellationToken cancellationToken = default)
    {
        if (await db.VendorInvoices.AnyAsync(x => x.VendorId == vendorId && x.InvoiceNumber == invoiceNumber.Trim(), cancellationToken))
            return Result.Failure<VendorInvoice>("Duplicate vendor invoice number.");

        var create = VendorInvoice.Create(facilityId, vendorId, invoiceNumber, amount, currency, purchaseOrderId, goodsReceiptId);
        if (create.IsFailure) return create;
        db.VendorInvoices.Add(create.Value!);
        await auditWriter.WriteAsync("FIN", "CaptureInvoice", nameof(VendorInvoice), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<VendorInvoice>> MatchAsync(Guid invoiceId, CancellationToken cancellationToken = default)
    {
        var invoice = await db.VendorInvoices.FirstOrDefaultAsync(x => x.Id == invoiceId, cancellationToken);
        if (invoice is null) return Result.Failure<VendorInvoice>("Invoice not found.");
        var match = invoice.Match();
        if (match.IsFailure) return Result.Failure<VendorInvoice>(match.Error!);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(invoice);
    }
}
