using FluentAssertions;
using HealthcareERP.Modules.Hms.Domain;

namespace HealthcareERP.UnitTests;

public class HmsOpsTests
{
    [Fact]
    public void Bed_CannotDoubleOccupy()
    {
        var bed = Bed.Create(Guid.NewGuid(), "B1", "Ward A", "General");
        bed.IsSuccess.Should().BeTrue();
        bed.Value!.Occupy().IsSuccess.Should().BeTrue();
        bed.Value.Occupy().IsFailure.Should().BeTrue();
    }

    [Fact]
    public void OtCase_RequiresChecklistBeforeComplete()
    {
        var ot = OtCase.Schedule(Guid.NewGuid(), Guid.NewGuid(), Guid.NewGuid(), "OT1", "Appendectomy", DateTimeOffset.UtcNow);
        ot.IsSuccess.Should().BeTrue();
        ot.Value!.Complete().IsFailure.Should().BeTrue();
        ot.Value.CompleteChecklist().IsSuccess.Should().BeTrue();
        ot.Value.Complete().IsSuccess.Should().BeTrue();
    }

    [Fact]
    public void ErEncounter_AllowsUnidentifiedPatient()
    {
        var er = ErEncounter.Open(Guid.NewGuid(), null, null);
        er.IsSuccess.Should().BeTrue();
        er.Value!.TemporaryId.Should().StartWith("UNK-");
    }

    [Fact]
    public void Discharge_RequiresSummary()
    {
        var d = DischargeProcess.Initiate(Guid.NewGuid(), Guid.NewGuid(), Guid.NewGuid());
        d.IsSuccess.Should().BeTrue();
        d.Value!.Complete(" ", null).IsFailure.Should().BeTrue();
        d.Value.Complete("Recovered, follow up in 7 days", null).IsSuccess.Should().BeTrue();
    }

    [Fact]
    public void MarEntry_AdministeredIsImmutable()
    {
        var mar = MarEntry.Schedule(
            Guid.NewGuid(), Guid.NewGuid(), Guid.NewGuid(), Guid.NewGuid(), Guid.NewGuid(),
            "DOSE-1", "Paracetamol");
        mar.IsSuccess.Should().BeTrue();
        mar.Value!.Administer(null).IsSuccess.Should().BeTrue();
        mar.Value.Administer("again").IsFailure.Should().BeTrue();
        mar.Value.Hold("nope").IsFailure.Should().BeTrue();
    }

    [Fact]
    public void LabOrder_AdapterImportThenFinalize()
    {
        var order = LabOrder.Accept(Guid.NewGuid(), Guid.NewGuid(), "CBC", "Complete Blood Count", null);
        order.IsSuccess.Should().BeTrue();
        order.Value!.CollectSample(null).IsSuccess.Should().BeTrue();
        order.Value.ImportFromAdapter("Hb 13.2", false, "StubLabAnalyzer").IsSuccess.Should().BeTrue();
        order.Value.Status.Should().Be("Preliminary");
        order.Value.Finalize("Hb 13.2", false).IsSuccess.Should().BeTrue();
        order.Value.Status.Should().Be("Final");
    }

    [Fact]
    public void RadiologyOrder_AcquireThenSign()
    {
        var order = RadiologyOrder.Accept(Guid.NewGuid(), Guid.NewGuid(), "CT", "CT Head", null);
        order.IsSuccess.Should().BeTrue();
        order.Value!.AcquireFromAdapter("1.2.3.stub", "StubPacs").IsSuccess.Should().BeTrue();
        order.Value.StudyInstanceUid.Should().Be("1.2.3.stub");
        order.Value.SignReport("No acute findings.").IsSuccess.Should().BeTrue();
    }
}
