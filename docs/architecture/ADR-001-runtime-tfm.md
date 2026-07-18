# ADR-001 — Runtime TFM (.NET 9 now, .NET 10 path)

## Status
Accepted

## Context
The delivery baseline targets .NET 10, but the build agent currently has SDK `9.0.314` only (no `net10.0` SDK installed).

## Decision
Scaffold and implement the modular monolith on **`net9.0`** now. Keep package versions compatible with a straightforward TFM bump to **`net10.0`** when the SDK is available.

## Consequences
- Solution builds on the current machine.
- README and Directory.Build.props document the bump steps.
- No intentional use of .NET 9-only APIs that block a move to .NET 10.
