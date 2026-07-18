using FluentAssertions;
using HealthcareERP.Modules.Hris.Domain;

namespace HealthcareERP.UnitTests;

public class HrisTests
{
    [Fact]
    public void Credential_RequiresVerifyBeforeSchedulable()
    {
        var credential = Credential.Create(
            Guid.NewGuid(),
            Guid.NewGuid(),
            "License",
            "MED-1",
            "General Medicine",
            DateOnly.FromDateTime(DateTime.UtcNow.AddYears(-1)),
            DateOnly.FromDateTime(DateTime.UtcNow.AddYears(1)));

        credential.IsSuccess.Should().BeTrue();
        credential.Value!.Status.Should().Be("Submitted");
        credential.Value.IsSchedulable.Should().BeFalse();
        credential.Value.Verify().IsSuccess.Should().BeTrue();
        credential.Value.IsSchedulable.Should().BeTrue();
    }

    [Fact]
    public void PayrollRun_PostsFromCalculated()
    {
        var run = PayrollRun.Create(Guid.NewGuid(), "2026-07", 10000m, 1500m);
        run.IsSuccess.Should().BeTrue();
        run.Value!.NetAmount.Should().Be(8500m);
        run.Value.Post().IsSuccess.Should().BeTrue();
        run.Value.Status.Should().Be("Posted");
    }

    [Fact]
    public void LeaveRequest_RejectsInvertedDates()
    {
        var leave = LeaveRequest.Submit(
            Guid.NewGuid(),
            Guid.NewGuid(),
            "Annual",
            DateOnly.FromDateTime(DateTime.UtcNow.AddDays(5)),
            DateOnly.FromDateTime(DateTime.UtcNow),
            null);
        leave.IsFailure.Should().BeTrue();
    }
}
