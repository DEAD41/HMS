namespace HealthcareERP.Modules.Hms.Integration;

public interface ILabAnalyzerAdapter
{
    Task<LabAnalyzerImportResult> ImportAsync(string testCode, string? rawPayload, CancellationToken cancellationToken = default);
}

public sealed record LabAnalyzerImportResult(bool Success, string ResultValue, bool IsCritical, string? Error);

public sealed class StubLabAnalyzerAdapter : ILabAnalyzerAdapter
{
    public Task<LabAnalyzerImportResult> ImportAsync(string testCode, string? rawPayload, CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrWhiteSpace(testCode))
            return Task.FromResult(new LabAnalyzerImportResult(false, string.Empty, false, "Test code required."));

        var critical = rawPayload?.Contains("CRIT", StringComparison.OrdinalIgnoreCase) == true
            || testCode.Equals("TROP", StringComparison.OrdinalIgnoreCase);
        var value = string.IsNullOrWhiteSpace(rawPayload)
            ? $"STUB-{testCode.ToUpperInvariant()}-OK"
            : rawPayload.Trim();
        return Task.FromResult(new LabAnalyzerImportResult(true, value, critical, null));
    }
}
