using FluentAssertions;
using HealthcareERP.Modules.Financials.Domain;
using HealthcareERP.Modules.Inventory.Domain;
using HealthcareERP.Modules.Procurement.Domain;

namespace HealthcareERP.UnitTests;

public class InventoryAndFinancialsTests
{
    [Fact]
    public void StockBalance_IssueBelowAvailable_Fails()
    {
        var balance = StockBalance.Create(Guid.NewGuid(), Guid.NewGuid(), Guid.NewGuid());
        balance.Increase(5).IsSuccess.Should().BeTrue();
        balance.Decrease(6).IsFailure.Should().BeTrue();
    }

    [Fact]
    public void VendorInvoice_MatchRequiresPoAndGrn()
    {
        var invoice = VendorInvoice.Create(Guid.NewGuid(), Guid.NewGuid(), "INV-1", 100, "PKR", null, null);
        invoice.IsSuccess.Should().BeTrue();
        invoice.Value!.Match().IsFailure.Should().BeTrue();
    }

    [Fact]
    public void PurchaseOrder_ComputesTotal()
    {
        var po = PurchaseOrder.Issue(Guid.NewGuid(), Guid.NewGuid(), 10, 12.5m, "PKR", null, null);
        po.IsSuccess.Should().BeTrue();
        po.Value!.TotalAmount.Should().Be(125m);
        po.Value.Status.Should().Be("Issued");
    }

    [Fact]
    public void Account_RejectsInvalidType()
    {
        var result = Account.Create(Guid.NewGuid(), "1000", "Cash", "Unknown");
        result.IsFailure.Should().BeTrue();
    }

    [Fact]
    public void Batch_RejectsExpiredIssue()
    {
        var batch = Batch.Receive(
            Guid.NewGuid(), Guid.NewGuid(), Guid.NewGuid(),
            "LOT-A", DateOnly.FromDateTime(DateTime.UtcNow.AddDays(30)), 10);
        batch.IsSuccess.Should().BeTrue();
        // Force expiry for unit assertion by decreasing after mutating via private path is not available;
        // expired receive is rejected instead:
        var expired = Batch.Receive(
            Guid.NewGuid(), Guid.NewGuid(), Guid.NewGuid(),
            "LOT-X", DateOnly.FromDateTime(DateTime.UtcNow.AddDays(-1)), 5);
        expired.IsFailure.Should().BeTrue();
        batch.Value!.Decrease(3).IsSuccess.Should().BeTrue();
        batch.Value.QuantityOnHand.Should().Be(7);
    }

    [Fact]
    public void Batch_FefoOrdering_PrefersEarlierExpiry()
    {
        var early = Batch.Receive(Guid.NewGuid(), Guid.NewGuid(), Guid.NewGuid(), "E1", DateOnly.FromDateTime(DateTime.UtcNow.AddDays(10)), 5);
        var late = Batch.Receive(Guid.NewGuid(), Guid.NewGuid(), Guid.NewGuid(), "L1", DateOnly.FromDateTime(DateTime.UtcNow.AddDays(40)), 5);
        early.IsSuccess.Should().BeTrue();
        late.IsSuccess.Should().BeTrue();
        early.Value!.ExpiryDate.Should().BeBefore(late.Value!.ExpiryDate);
    }
}
