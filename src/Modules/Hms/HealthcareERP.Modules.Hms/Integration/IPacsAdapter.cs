namespace HealthcareERP.Modules.Hms.Integration;

public interface IPacsAdapter
{
    Task<PacsStudyStatus> AcquireAsync(string accessionNumber, string modality, CancellationToken cancellationToken = default);
}

public sealed record PacsStudyStatus(bool Success, string StudyInstanceUid, string Status, string? Error);

public sealed class StubPacsAdapter : IPacsAdapter
{
    public Task<PacsStudyStatus> AcquireAsync(string accessionNumber, string modality, CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrWhiteSpace(accessionNumber))
            return Task.FromResult(new PacsStudyStatus(false, string.Empty, "Failed", "Accession required."));

        var uid = $"1.2.826.stub.{modality.ToUpperInvariant()}.{Guid.NewGuid():N}";
        return Task.FromResult(new PacsStudyStatus(true, uid, "Acquired", null));
    }
}
