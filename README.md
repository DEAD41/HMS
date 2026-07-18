# Healthcare ERP (Modular Monolith)

Integrated Healthcare Enterprise Software covering **HMS, HRIS, Financials, Inventory, Procurement**, and a shared **Foundation** integration hub.

## Documentation
- Blueprint: [`Healthcare-ERP-Pathway-and-Workflow.md`](Healthcare-ERP-Pathway-and-Workflow.md)
- Requirements library: [`docs/requirements/README.md`](docs/requirements/README.md)
- Verification package: [`docs/requirements/VERIFICATION.md`](docs/requirements/VERIFICATION.md)
- Architecture ADRs: [`docs/architecture/`](docs/architecture/)

## Stack
| Layer | Choice |
|---|---|
| API | ASP.NET Core (`net9.0`, bump path to `net10.0` — see ADR-001) |
| UI | React + TypeScript (Vite) |
| DB | PostgreSQL 17 in local Docker Compose |
| Architecture | Modular monolith + outbox/inbox integration events |

## Solution layout
```
src/
  BuildingBlocks/
  Host/HealthcareERP.Api/
  Modules/{Foundation,Hms,Hris,Financials,Inventory,Procurement}/
frontend/
docs/requirements/
tests/
```

## Local Docker build (primary workflow)
```powershell
.\scripts\build-local-docker.ps1
docker compose ps
```

- API: `http://localhost:5080`
- Swagger: `http://localhost:5080/swagger`
- PostgreSQL: `localhost:5433` (mapped from container `5432`)

The React UI is an optional Compose profile because it pulls Node and Nginx
from Docker Hub:
```bash
docker compose --profile ui up --build -d
```
Application: `http://localhost:5173`

Stop the stack without deleting data:
```bash
docker compose down
```

Reset all local database data:
```bash
docker compose down -v
```

Compose creates module-owned databases on one PostgreSQL server:
- `healthcare_erp_foundation`
- `healthcare_erp_hms`
- `healthcare_erp_hris`
- `healthcare_erp_financials`
- `healthcare_erp_inventory`
- `healthcare_erp_procurement`

## Backend verification
```bash
docker compose build api
docker compose run --rm api --help
dotnet test HealthcareERP.sln
```

The script builds/tests with the locally installed SDK, publishes to
`artifacts/api`, and packages that output in the Docker runtime image. This
keeps builds working even when Docker Desktop's internal DNS cannot reach
NuGet. The direct-host development profile keeps `Database:UseInMemory=true`
for fast integration tests; Docker overrides it to `false` and uses PostgreSQL.

## Build increments (gated)
1. Foundation hub — **implemented (MVP)** — approved (Inc 1)
2. HMS core (registration, appointments, OPD, billing charges) — **implemented (MVP)** — approved (Inc 1)
3. Financials + Inventory + Procurement — **implemented (MVP)** — approved (Inc 2)
4. HMS operational sub-modules (IPD/ER/OT/LIS/RIS/pharmacy/discharge) — **implemented (MVP)** — approved (Inc 3)
5. HRIS (employee/credentials/roster/leave/payroll) — **implemented (MVP)** — approved (Inc 4)
6. Optimization / portals / MIS (auth, budgets, MIS, vendor scorecards, ESS) — **implemented (MVP)** — approved (Inc 5)
7. Clinical depth (batch/FEFO, MAR/care plans, LIS/RIS stub adapters) — **implemented (MVP)** — awaiting approval

Acceptance checklists:
- [`docs/architecture/ACCEPTANCE-INCREMENT-01.md`](docs/architecture/ACCEPTANCE-INCREMENT-01.md) — approved
- [`docs/architecture/ACCEPTANCE-INCREMENT-02.md`](docs/architecture/ACCEPTANCE-INCREMENT-02.md) — approved
- [`docs/architecture/ACCEPTANCE-INCREMENT-03.md`](docs/architecture/ACCEPTANCE-INCREMENT-03.md) — approved
- [`docs/architecture/ACCEPTANCE-INCREMENT-04.md`](docs/architecture/ACCEPTANCE-INCREMENT-04.md) — approved
- [`docs/architecture/ACCEPTANCE-INCREMENT-05.md`](docs/architecture/ACCEPTANCE-INCREMENT-05.md) — approved
- [`docs/architecture/ACCEPTANCE-INCREMENT-06.md`](docs/architecture/ACCEPTANCE-INCREMENT-06.md) — pending

### Sample users (Increment 5)
| Username | Password | Roles |
|---|---|---|
| `admin` | `Admin@123` | Admin + all demo roles |
| `doctor` | `Doctor@123` | Clinician |
| `hr` | `Hr@123` | Hr |
| `finance` | `Finance@123` | Finance |
| `employee` | `Employee@123` | Employee (ESS) |

Login: Swagger `POST /api/fnd/auth/login` or UI at `http://localhost:5173` (optional Compose profile `ui`).

Each increment maps to requirement IDs under `docs/requirements/` and stops for acceptance review.
