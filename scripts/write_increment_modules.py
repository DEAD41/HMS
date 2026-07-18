#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def w(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print("wrote", rel)


# ---------- Financials ----------
w(
    "src/Modules/Financials/HealthcareERP.Modules.Financials.Contracts/Events/JournalPosted.cs",
    """
namespace HealthcareERP.Modules.Financials.Contracts.Events;

public sealed record JournalPosted(Guid JournalId, Guid FacilityId, string SourceDocumentId, decimal TotalDebit);
""",
)

w(
    "src/Modules/Financials/HealthcareERP.Modules.Financials/Domain/Account.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Financials.Domain;

public sealed class Account : AggregateRoot
{
    private Account() { }

    public Guid FacilityId { get; private set; }
    public string Code { get; private set; } = string.Empty;
    public string Name { get; private set; } = string.Empty;
    public string Type { get; private set; } = "Asset";
    public string Status { get; private set; } = "Active";

    public static Result<Account> Create(Guid facilityId, string code, string name, string type)
    {
        var allowed = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
            { "Asset", "Liability", "Equity", "Revenue", "Expense" };
        if (facilityId == Guid.Empty) return Result.Failure<Account>("Facility is required.");
        if (string.IsNullOrWhiteSpace(code)) return Result.Failure<Account>("Account code is required.");
        if (string.IsNullOrWhiteSpace(name)) return Result.Failure<Account>("Account name is required.");
        if (!allowed.Contains(type)) return Result.Failure<Account>("Invalid account type.");

        return Result.Success(new Account
        {
            FacilityId = facilityId,
            Code = code.Trim().ToUpperInvariant(),
            Name = name.Trim(),
            Type = type,
            Status = "Active"
        });
    }
}
""",
)

w(
    "src/Modules/Financials/HealthcareERP.Modules.Financials/Domain/CostCenter.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Financials.Domain;

public sealed class CostCenter : AggregateRoot
{
    private CostCenter() { }

    public Guid FacilityId { get; private set; }
    public string Code { get; private set; } = string.Empty;
    public string Name { get; private set; } = string.Empty;
    public string Status { get; private set; } = "Active";

    public static Result<CostCenter> Create(Guid facilityId, string code, string name)
    {
        if (facilityId == Guid.Empty) return Result.Failure<CostCenter>("Facility is required.");
        if (string.IsNullOrWhiteSpace(code)) return Result.Failure<CostCenter>("Cost center code is required.");
        if (string.IsNullOrWhiteSpace(name)) return Result.Failure<CostCenter>("Cost center name is required.");

        return Result.Success(new CostCenter
        {
            FacilityId = facilityId,
            Code = code.Trim().ToUpperInvariant(),
            Name = name.Trim(),
            Status = "Active"
        });
    }
}
""",
)

w(
    "src/Modules/Financials/HealthcareERP.Modules.Financials/Domain/Receivable.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Financials.Domain;

public sealed class Receivable : AggregateRoot
{
    private Receivable() { }

    public Guid FacilityId { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid SourceChargeId { get; private set; }
    public string ChargeCode { get; private set; } = string.Empty;
    public decimal Amount { get; private set; }
    public string Currency { get; private set; } = "USD";
    public string Status { get; private set; } = "Open";
    public decimal SettledAmount { get; private set; }

    public static Result<Receivable> FromCharge(
        Guid facilityId,
        Guid patientId,
        Guid sourceChargeId,
        string chargeCode,
        decimal amount,
        string currency)
    {
        if (amount < 0) return Result.Failure<Receivable>("Amount cannot be negative.");
        return Result.Success(new Receivable
        {
            FacilityId = facilityId,
            PatientId = patientId,
            SourceChargeId = sourceChargeId,
            ChargeCode = chargeCode.Trim().ToUpperInvariant(),
            Amount = amount,
            Currency = currency.Trim().ToUpperInvariant(),
            Status = "Open"
        });
    }

    public Result ApplyPayment(decimal amount)
    {
        if (amount <= 0) return Result.Failure("Payment must be positive.");
        SettledAmount += amount;
        Status = SettledAmount >= Amount ? "Settled" : "PartiallySettled";
        Touch();
        return Result.Success();
    }
}
""",
)

w(
    "src/Modules/Financials/HealthcareERP.Modules.Financials/Domain/VendorInvoice.cs",
    """
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
""",
)

w(
    "src/Modules/Financials/HealthcareERP.Modules.Financials/Persistence/FinancialsDbContext.cs",
    """
using HealthcareERP.Modules.Financials.Domain;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Financials.Persistence;

public sealed class FinancialsDbContext(DbContextOptions<FinancialsDbContext> options) : DbContext(options)
{
    public DbSet<Account> Accounts => Set<Account>();
    public DbSet<CostCenter> CostCenters => Set<CostCenter>();
    public DbSet<Receivable> Receivables => Set<Receivable>();
    public DbSet<VendorInvoice> VendorInvoices => Set<VendorInvoice>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.HasDefaultSchema("fin");

        modelBuilder.Entity<Account>(b =>
        {
            b.ToTable("accounts");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.FacilityId, x.Code }).IsUnique();
            b.Property(x => x.Code).HasMaxLength(32);
            b.Property(x => x.Name).HasMaxLength(200);
            b.Property(x => x.Type).HasMaxLength(32);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<CostCenter>(b =>
        {
            b.ToTable("cost_centers");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.FacilityId, x.Code }).IsUnique();
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<Receivable>(b =>
        {
            b.ToTable("receivables");
            b.HasKey(x => x.Id);
            b.HasIndex(x => x.SourceChargeId).IsUnique();
            b.Property(x => x.Amount).HasPrecision(18, 2);
            b.Property(x => x.SettledAmount).HasPrecision(18, 2);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<VendorInvoice>(b =>
        {
            b.ToTable("vendor_invoices");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.VendorId, x.InvoiceNumber }).IsUnique();
            b.Property(x => x.Amount).HasPrecision(18, 2);
            b.Ignore(x => x.DomainEvents);
        });
    }
}
""",
)

w(
    "src/Modules/Financials/HealthcareERP.Modules.Financials/Services/LedgerService.cs",
    """
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Financials.Domain;
using HealthcareERP.Modules.Financials.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Financials.Services;

public sealed class LedgerService(FinancialsDbContext db, IAuditWriter auditWriter)
{
    public async Task<Result<Account>> CreateAccountAsync(Guid facilityId, string code, string name, string type, CancellationToken cancellationToken = default)
    {
        if (await db.Accounts.AnyAsync(x => x.FacilityId == facilityId && x.Code == code.Trim().ToUpperInvariant(), cancellationToken))
            return Result.Failure<Account>("Account code already exists.");

        var create = Account.Create(facilityId, code, name, type);
        if (create.IsFailure) return create;
        db.Accounts.Add(create.Value!);
        await auditWriter.WriteAsync("FIN", "Create", nameof(Account), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public Task<List<Account>> ListAccountsAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.Accounts.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderBy(x => x.Code).ToListAsync(cancellationToken);

    public async Task<Result<CostCenter>> CreateCostCenterAsync(Guid facilityId, string code, string name, CancellationToken cancellationToken = default)
    {
        if (await db.CostCenters.AnyAsync(x => x.FacilityId == facilityId && x.Code == code.Trim().ToUpperInvariant(), cancellationToken))
            return Result.Failure<CostCenter>("Cost center code already exists.");

        var create = CostCenter.Create(facilityId, code, name);
        if (create.IsFailure) return create;
        db.CostCenters.Add(create.Value!);
        await auditWriter.WriteAsync("FIN", "Create", nameof(CostCenter), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }
}
""",
)

w(
    "src/Modules/Financials/HealthcareERP.Modules.Financials/Services/ReceivableService.cs",
    """
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Financials.Domain;
using HealthcareERP.Modules.Financials.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Financials.Services;

public sealed class ReceivableService(FinancialsDbContext db, IAuditWriter auditWriter)
{
    public async Task<Result<Receivable>> CreateFromChargeAsync(
        Guid facilityId,
        Guid patientId,
        Guid sourceChargeId,
        string chargeCode,
        decimal amount,
        string currency,
        CancellationToken cancellationToken = default)
    {
        var existing = await db.Receivables.FirstOrDefaultAsync(x => x.SourceChargeId == sourceChargeId, cancellationToken);
        if (existing is not null) return Result.Success(existing);

        var create = Receivable.FromCharge(facilityId, patientId, sourceChargeId, chargeCode, amount, currency);
        if (create.IsFailure) return create;
        db.Receivables.Add(create.Value!);
        await auditWriter.WriteAsync("FIN", "OpenReceivable", nameof(Receivable), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public Task<List<Receivable>> ListAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.Receivables.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderByDescending(x => x.CreatedAt).ToListAsync(cancellationToken);
}
""",
)

w(
    "src/Modules/Financials/HealthcareERP.Modules.Financials/Services/AccountsPayableService.cs",
    """
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
""",
)

w(
    "src/Modules/Financials/HealthcareERP.Modules.Financials/Integration/BillableEventCreatedHandler.cs",
    """
using System.Text.Json;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Infrastructure.Outbox;
using HealthcareERP.Modules.Financials.Services;

namespace HealthcareERP.Modules.Financials.Integration;

public sealed class BillableEventCreatedHandler(ReceivableService receivableService) : IIntegrationEventHandler
{
    public string EventType => "BillableEventCreated";

    public async Task HandleAsync(IntegrationEvent integrationEvent, CancellationToken cancellationToken = default)
    {
        using var doc = JsonDocument.Parse(integrationEvent.PayloadJson);
        var root = doc.RootElement;
        var chargeId = root.GetProperty("Id").GetGuid();
        var patientId = root.GetProperty("PatientId").GetGuid();
        var chargeCode = root.GetProperty("ChargeCode").GetString() ?? "CHARGE";
        var amount = root.GetProperty("Amount").GetDecimal();
        var currency = root.GetProperty("Currency").GetString() ?? "USD";

        var result = await receivableService.CreateFromChargeAsync(
            integrationEvent.FacilityId,
            patientId,
            chargeId,
            chargeCode,
            amount,
            currency,
            cancellationToken);

        if (result.IsFailure)
            throw new InvalidOperationException(result.Error);
    }
}
""",
)

w(
    "src/Modules/Financials/HealthcareERP.Modules.Financials/DependencyInjection.cs",
    """
using HealthcareERP.BuildingBlocks.Infrastructure.Outbox;
using HealthcareERP.Modules.Financials.Integration;
using HealthcareERP.Modules.Financials.Persistence;
using HealthcareERP.Modules.Financials.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace HealthcareERP.Modules.Financials;

public static class DependencyInjection
{
    public static IServiceCollection AddFinancialsModule(this IServiceCollection services, string? connectionString, bool useInMemory = false)
    {
        if (useInMemory || string.IsNullOrWhiteSpace(connectionString))
            services.AddDbContext<FinancialsDbContext>(o => o.UseInMemoryDatabase("healthcare-erp-fin"));
        else
            services.AddDbContext<FinancialsDbContext>(o => o.UseNpgsql(connectionString));

        services.AddScoped<LedgerService>();
        services.AddScoped<ReceivableService>();
        services.AddScoped<AccountsPayableService>();
        services.AddScoped<IIntegrationEventHandler, BillableEventCreatedHandler>();
        return services;
    }
}
""",
)

# ---------- Inventory ----------
w(
    "src/Modules/Inventory/HealthcareERP.Modules.Inventory.Contracts/Events/StockAvailabilityChanged.cs",
    """
namespace HealthcareERP.Modules.Inventory.Contracts.Events;

public sealed record StockAvailabilityChanged(Guid ItemId, Guid StoreId, decimal QuantityOnHand, bool BelowReorder);
""",
)

w(
    "src/Modules/Inventory/HealthcareERP.Modules.Inventory/Domain/Item.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Inventory.Domain;

public sealed class Item : AggregateRoot
{
    private Item() { }

    public Guid FacilityId { get; private set; }
    public string Sku { get; private set; } = string.Empty;
    public string Name { get; private set; } = string.Empty;
    public string UnitOfMeasure { get; private set; } = "EA";
    public bool BatchControlled { get; private set; }
    public decimal ReorderLevel { get; private set; }
    public string Status { get; private set; } = "Active";

    public static Result<Item> Create(Guid facilityId, string sku, string name, string uom, bool batchControlled, decimal reorderLevel)
    {
        if (string.IsNullOrWhiteSpace(sku)) return Result.Failure<Item>("SKU is required.");
        if (string.IsNullOrWhiteSpace(name)) return Result.Failure<Item>("Name is required.");
        if (reorderLevel < 0) return Result.Failure<Item>("Reorder level cannot be negative.");

        return Result.Success(new Item
        {
            FacilityId = facilityId,
            Sku = sku.Trim().ToUpperInvariant(),
            Name = name.Trim(),
            UnitOfMeasure = uom.Trim().ToUpperInvariant(),
            BatchControlled = batchControlled,
            ReorderLevel = reorderLevel,
            Status = "Active"
        });
    }
}
""",
)

w(
    "src/Modules/Inventory/HealthcareERP.Modules.Inventory/Domain/Store.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Inventory.Domain;

public sealed class Store : AggregateRoot
{
    private Store() { }

    public Guid FacilityId { get; private set; }
    public string Code { get; private set; } = string.Empty;
    public string Name { get; private set; } = string.Empty;
    public string Status { get; private set; } = "Active";

    public static Result<Store> Create(Guid facilityId, string code, string name)
    {
        if (string.IsNullOrWhiteSpace(code)) return Result.Failure<Store>("Store code is required.");
        if (string.IsNullOrWhiteSpace(name)) return Result.Failure<Store>("Store name is required.");
        return Result.Success(new Store
        {
            FacilityId = facilityId,
            Code = code.Trim().ToUpperInvariant(),
            Name = name.Trim(),
            Status = "Active"
        });
    }
}
""",
)

w(
    "src/Modules/Inventory/HealthcareERP.Modules.Inventory/Domain/StockBalance.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Inventory.Domain;

public sealed class StockBalance : AggregateRoot
{
    private StockBalance() { }

    public Guid FacilityId { get; private set; }
    public Guid StoreId { get; private set; }
    public Guid ItemId { get; private set; }
    public decimal QuantityOnHand { get; private set; }

    public static StockBalance Create(Guid facilityId, Guid storeId, Guid itemId) => new()
    {
        FacilityId = facilityId,
        StoreId = storeId,
        ItemId = itemId,
        QuantityOnHand = 0
    };

    public Result Increase(decimal qty)
    {
        if (qty <= 0) return Result.Failure("Quantity must be positive.");
        QuantityOnHand += qty;
        Touch();
        return Result.Success();
    }

    public Result Decrease(decimal qty)
    {
        if (qty <= 0) return Result.Failure("Quantity must be positive.");
        if (qty > QuantityOnHand) return Result.Failure("Insufficient stock.");
        QuantityOnHand -= qty;
        Touch();
        return Result.Success();
    }
}
""",
)

w(
    "src/Modules/Inventory/HealthcareERP.Modules.Inventory/Persistence/InventoryDbContext.cs",
    """
using HealthcareERP.Modules.Inventory.Domain;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Inventory.Persistence;

public sealed class InventoryDbContext(DbContextOptions<InventoryDbContext> options) : DbContext(options)
{
    public DbSet<Item> Items => Set<Item>();
    public DbSet<Store> Stores => Set<Store>();
    public DbSet<StockBalance> StockBalances => Set<StockBalance>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.HasDefaultSchema("inv");

        modelBuilder.Entity<Item>(b =>
        {
            b.ToTable("items");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.FacilityId, x.Sku }).IsUnique();
            b.Property(x => x.ReorderLevel).HasPrecision(18, 2);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<Store>(b =>
        {
            b.ToTable("stores");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.FacilityId, x.Code }).IsUnique();
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<StockBalance>(b =>
        {
            b.ToTable("stock_balances");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.StoreId, x.ItemId }).IsUnique();
            b.Property(x => x.QuantityOnHand).HasPrecision(18, 2);
            b.Ignore(x => x.DomainEvents);
        });
    }
}
""",
)

w(
    "src/Modules/Inventory/HealthcareERP.Modules.Inventory/Services/InventoryService.cs",
    """
using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Inventory.Contracts.Events;
using HealthcareERP.Modules.Inventory.Domain;
using HealthcareERP.Modules.Inventory.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Inventory.Services;

public sealed class InventoryService(
    InventoryDbContext db,
    IIntegrationEventPublisher publisher,
    IAuditWriter auditWriter)
{
    public async Task<Result<Item>> CreateItemAsync(Guid facilityId, string sku, string name, string uom, bool batchControlled, decimal reorderLevel, CancellationToken cancellationToken = default)
    {
        if (await db.Items.AnyAsync(x => x.FacilityId == facilityId && x.Sku == sku.Trim().ToUpperInvariant(), cancellationToken))
            return Result.Failure<Item>("SKU already exists.");

        var create = Item.Create(facilityId, sku, name, uom, batchControlled, reorderLevel);
        if (create.IsFailure) return create;
        db.Items.Add(create.Value!);
        await auditWriter.WriteAsync("INV", "Create", nameof(Item), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<Store>> CreateStoreAsync(Guid facilityId, string code, string name, CancellationToken cancellationToken = default)
    {
        if (await db.Stores.AnyAsync(x => x.FacilityId == facilityId && x.Code == code.Trim().ToUpperInvariant(), cancellationToken))
            return Result.Failure<Store>("Store code already exists.");

        var create = Store.Create(facilityId, code, name);
        if (create.IsFailure) return create;
        db.Stores.Add(create.Value!);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<StockBalance>> ReceiveAsync(Guid facilityId, Guid storeId, Guid itemId, decimal quantity, CancellationToken cancellationToken = default)
    {
        var item = await db.Items.FirstOrDefaultAsync(x => x.Id == itemId && x.FacilityId == facilityId, cancellationToken);
        if (item is null) return Result.Failure<StockBalance>("Item not found.");
        if (!await db.Stores.AnyAsync(x => x.Id == storeId && x.FacilityId == facilityId, cancellationToken))
            return Result.Failure<StockBalance>("Store not found.");

        var balance = await db.StockBalances.FirstOrDefaultAsync(x => x.StoreId == storeId && x.ItemId == itemId, cancellationToken);
        if (balance is null)
        {
            balance = StockBalance.Create(facilityId, storeId, itemId);
            db.StockBalances.Add(balance);
        }

        var increase = balance.Increase(quantity);
        if (increase.IsFailure) return Result.Failure<StockBalance>(increase.Error!);

        await PublishAvailabilityAsync(item, balance, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(balance);
    }

    public async Task<Result<StockBalance>> IssueAsync(Guid facilityId, Guid storeId, Guid itemId, decimal quantity, CancellationToken cancellationToken = default)
    {
        var item = await db.Items.FirstOrDefaultAsync(x => x.Id == itemId && x.FacilityId == facilityId, cancellationToken);
        if (item is null) return Result.Failure<StockBalance>("Item not found.");

        var balance = await db.StockBalances.FirstOrDefaultAsync(x => x.StoreId == storeId && x.ItemId == itemId, cancellationToken);
        if (balance is null) return Result.Failure<StockBalance>("No stock balance.");

        var decrease = balance.Decrease(quantity);
        if (decrease.IsFailure) return Result.Failure<StockBalance>(decrease.Error!);

        await PublishAvailabilityAsync(item, balance, cancellationToken);

        if (balance.QuantityOnHand <= item.ReorderLevel)
        {
            await publisher.EnqueueAsync(new IntegrationEvent(
                Guid.NewGuid(),
                "PurchaseRequisitionRequested",
                "v1",
                DateTimeOffset.UtcNow,
                null,
                null,
                facilityId,
                item.Id.ToString(),
                JsonSerializer.Serialize(new
                {
                    SignalId = Guid.NewGuid(),
                    ItemId = item.Id,
                    StoreId = storeId,
                    SuggestedQty = Math.Max(item.ReorderLevel * 2 - balance.QuantityOnHand, 1),
                    item.Sku,
                    item.Name
                })), cancellationToken);
        }

        await db.SaveChangesAsync(cancellationToken);
        return Result.Success(balance);
    }

    public Task<List<Item>> ListItemsAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.Items.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderBy(x => x.Sku).ToListAsync(cancellationToken);

    private async Task PublishAvailabilityAsync(Item item, StockBalance balance, CancellationToken cancellationToken)
    {
        var payload = new StockAvailabilityChanged(item.Id, balance.StoreId, balance.QuantityOnHand, balance.QuantityOnHand <= item.ReorderLevel);
        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(),
            "StockAvailabilityChanged",
            "v1",
            DateTimeOffset.UtcNow,
            null,
            null,
            item.FacilityId,
            item.Id.ToString(),
            JsonSerializer.Serialize(payload)), cancellationToken);
    }
}
""",
)

w(
    "src/Modules/Inventory/HealthcareERP.Modules.Inventory/DependencyInjection.cs",
    """
using HealthcareERP.Modules.Inventory.Persistence;
using HealthcareERP.Modules.Inventory.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace HealthcareERP.Modules.Inventory;

public static class DependencyInjection
{
    public static IServiceCollection AddInventoryModule(this IServiceCollection services, string? connectionString, bool useInMemory = false)
    {
        if (useInMemory || string.IsNullOrWhiteSpace(connectionString))
            services.AddDbContext<InventoryDbContext>(o => o.UseInMemoryDatabase("healthcare-erp-inv"));
        else
            services.AddDbContext<InventoryDbContext>(o => o.UseNpgsql(connectionString));

        services.AddScoped<InventoryService>();
        return services;
    }
}
""",
)

# ---------- Procurement ----------
w(
    "src/Modules/Procurement/HealthcareERP.Modules.Procurement.Contracts/Events/PurchaseOrderIssued.cs",
    """
namespace HealthcareERP.Modules.Procurement.Contracts.Events;

public sealed record PurchaseOrderIssued(Guid PurchaseOrderId, Guid VendorId, Guid FacilityId, decimal TotalAmount);
""",
)

w(
    "src/Modules/Procurement/HealthcareERP.Modules.Procurement/Domain/Vendor.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Procurement.Domain;

public sealed class Vendor : AggregateRoot
{
    private Vendor() { }

    public Guid FacilityId { get; private set; }
    public string Code { get; private set; } = string.Empty;
    public string Name { get; private set; } = string.Empty;
    public string Status { get; private set; } = "Active";

    public static Result<Vendor> Create(Guid facilityId, string code, string name)
    {
        if (string.IsNullOrWhiteSpace(code)) return Result.Failure<Vendor>("Vendor code is required.");
        if (string.IsNullOrWhiteSpace(name)) return Result.Failure<Vendor>("Vendor name is required.");
        return Result.Success(new Vendor
        {
            FacilityId = facilityId,
            Code = code.Trim().ToUpperInvariant(),
            Name = name.Trim(),
            Status = "Active"
        });
    }
}
""",
)

w(
    "src/Modules/Procurement/HealthcareERP.Modules.Procurement/Domain/PurchaseRequisition.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Procurement.Domain;

public sealed class PurchaseRequisition : AggregateRoot
{
    private PurchaseRequisition() { }

    public Guid FacilityId { get; private set; }
    public Guid? ItemId { get; private set; }
    public Guid? StoreId { get; private set; }
    public Guid? SignalId { get; private set; }
    public string Description { get; private set; } = string.Empty;
    public decimal Quantity { get; private set; }
    public string Status { get; private set; } = "Draft";

    public static Result<PurchaseRequisition> Create(
        Guid facilityId,
        string description,
        decimal quantity,
        Guid? itemId,
        Guid? storeId,
        Guid? signalId)
    {
        if (quantity <= 0) return Result.Failure<PurchaseRequisition>("Quantity must be positive.");
        return Result.Success(new PurchaseRequisition
        {
            FacilityId = facilityId,
            Description = description.Trim(),
            Quantity = quantity,
            ItemId = itemId,
            StoreId = storeId,
            SignalId = signalId,
            Status = "Approved"
        });
    }
}
""",
)

w(
    "src/Modules/Procurement/HealthcareERP.Modules.Procurement/Domain/PurchaseOrder.cs",
    """
using HealthcareERP.BuildingBlocks.Domain;

namespace HealthcareERP.Modules.Procurement.Domain;

public sealed class PurchaseOrder : AggregateRoot
{
    private PurchaseOrder() { }

    public Guid FacilityId { get; private set; }
    public Guid VendorId { get; private set; }
    public Guid? RequisitionId { get; private set; }
    public Guid? ItemId { get; private set; }
    public decimal Quantity { get; private set; }
    public decimal UnitPrice { get; private set; }
    public string Currency { get; private set; } = "USD";
    public string Status { get; private set; } = "Draft";

    public decimal TotalAmount => Quantity * UnitPrice;

    public static Result<PurchaseOrder> Issue(
        Guid facilityId,
        Guid vendorId,
        decimal quantity,
        decimal unitPrice,
        string currency,
        Guid? requisitionId,
        Guid? itemId)
    {
        if (quantity <= 0) return Result.Failure<PurchaseOrder>("Quantity must be positive.");
        if (unitPrice < 0) return Result.Failure<PurchaseOrder>("Unit price cannot be negative.");
        return Result.Success(new PurchaseOrder
        {
            FacilityId = facilityId,
            VendorId = vendorId,
            Quantity = quantity,
            UnitPrice = unitPrice,
            Currency = currency.Trim().ToUpperInvariant(),
            RequisitionId = requisitionId,
            ItemId = itemId,
            Status = "Issued"
        });
    }
}
""",
)

w(
    "src/Modules/Procurement/HealthcareERP.Modules.Procurement/Persistence/ProcurementDbContext.cs",
    """
using HealthcareERP.Modules.Procurement.Domain;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Procurement.Persistence;

public sealed class ProcurementDbContext(DbContextOptions<ProcurementDbContext> options) : DbContext(options)
{
    public DbSet<Vendor> Vendors => Set<Vendor>();
    public DbSet<PurchaseRequisition> PurchaseRequisitions => Set<PurchaseRequisition>();
    public DbSet<PurchaseOrder> PurchaseOrders => Set<PurchaseOrder>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.HasDefaultSchema("prc");

        modelBuilder.Entity<Vendor>(b =>
        {
            b.ToTable("vendors");
            b.HasKey(x => x.Id);
            b.HasIndex(x => new { x.FacilityId, x.Code }).IsUnique();
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<PurchaseRequisition>(b =>
        {
            b.ToTable("purchase_requisitions");
            b.HasKey(x => x.Id);
            b.HasIndex(x => x.SignalId);
            b.Property(x => x.Quantity).HasPrecision(18, 2);
            b.Ignore(x => x.DomainEvents);
        });

        modelBuilder.Entity<PurchaseOrder>(b =>
        {
            b.ToTable("purchase_orders");
            b.HasKey(x => x.Id);
            b.Property(x => x.Quantity).HasPrecision(18, 2);
            b.Property(x => x.UnitPrice).HasPrecision(18, 2);
            b.Ignore(x => x.DomainEvents);
            b.Ignore(x => x.TotalAmount);
        });
    }
}
""",
)

w(
    "src/Modules/Procurement/HealthcareERP.Modules.Procurement/Services/ProcurementService.cs",
    """
using System.Text.Json;
using HealthcareERP.BuildingBlocks.Application.Abstractions;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Domain;
using HealthcareERP.Modules.Procurement.Contracts.Events;
using HealthcareERP.Modules.Procurement.Domain;
using HealthcareERP.Modules.Procurement.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HealthcareERP.Modules.Procurement.Services;

public sealed class ProcurementService(
    ProcurementDbContext db,
    IIntegrationEventPublisher publisher,
    IAuditWriter auditWriter)
{
    public async Task<Result<Vendor>> CreateVendorAsync(Guid facilityId, string code, string name, CancellationToken cancellationToken = default)
    {
        if (await db.Vendors.AnyAsync(x => x.FacilityId == facilityId && x.Code == code.Trim().ToUpperInvariant(), cancellationToken))
            return Result.Failure<Vendor>("Vendor code already exists.");

        var create = Vendor.Create(facilityId, code, name);
        if (create.IsFailure) return create;
        db.Vendors.Add(create.Value!);
        await auditWriter.WriteAsync("PRC", "Create", nameof(Vendor), create.Value!.Id, null, null, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<PurchaseRequisition>> CreateRequisitionFromSignalAsync(
        Guid facilityId,
        Guid signalId,
        Guid itemId,
        Guid storeId,
        decimal quantity,
        string description,
        CancellationToken cancellationToken = default)
    {
        var existing = await db.PurchaseRequisitions.FirstOrDefaultAsync(x => x.SignalId == signalId, cancellationToken);
        if (existing is not null) return Result.Success(existing);

        var open = await db.PurchaseRequisitions.AnyAsync(x =>
            x.ItemId == itemId &&
            x.StoreId == storeId &&
            (x.Status == "Approved" || x.Status == "Draft"), cancellationToken);
        if (open) return Result.Failure<PurchaseRequisition>("Open requisition already exists for item/store.");

        var create = PurchaseRequisition.Create(facilityId, description, quantity, itemId, storeId, signalId);
        if (create.IsFailure) return create;
        db.PurchaseRequisitions.Add(create.Value!);
        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public async Task<Result<PurchaseOrder>> IssuePurchaseOrderAsync(
        Guid facilityId,
        Guid vendorId,
        Guid? requisitionId,
        Guid? itemId,
        decimal quantity,
        decimal unitPrice,
        string currency,
        CancellationToken cancellationToken = default)
    {
        if (!await db.Vendors.AnyAsync(x => x.Id == vendorId && x.Status == "Active", cancellationToken))
            return Result.Failure<PurchaseOrder>("Active vendor required.");

        var create = PurchaseOrder.Issue(facilityId, vendorId, quantity, unitPrice, currency, requisitionId, itemId);
        if (create.IsFailure) return create;
        db.PurchaseOrders.Add(create.Value!);

        var payload = new PurchaseOrderIssued(create.Value!.Id, vendorId, facilityId, create.Value.TotalAmount);
        await publisher.EnqueueAsync(new IntegrationEvent(
            Guid.NewGuid(),
            "PurchaseOrderIssued",
            "v1",
            DateTimeOffset.UtcNow,
            null,
            null,
            facilityId,
            create.Value.Id.ToString(),
            JsonSerializer.Serialize(payload)), cancellationToken);

        await db.SaveChangesAsync(cancellationToken);
        return create;
    }

    public Task<List<Vendor>> ListVendorsAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.Vendors.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderBy(x => x.Code).ToListAsync(cancellationToken);

    public Task<List<PurchaseRequisition>> ListRequisitionsAsync(Guid facilityId, CancellationToken cancellationToken = default) =>
        db.PurchaseRequisitions.AsNoTracking().Where(x => x.FacilityId == facilityId).OrderByDescending(x => x.CreatedAt).ToListAsync(cancellationToken);
}
""",
)

w(
    "src/Modules/Procurement/HealthcareERP.Modules.Procurement/Integration/PurchaseRequisitionRequestedHandler.cs",
    """
using System.Text.Json;
using HealthcareERP.BuildingBlocks.Contracts;
using HealthcareERP.BuildingBlocks.Infrastructure.Outbox;
using HealthcareERP.Modules.Procurement.Services;

namespace HealthcareERP.Modules.Procurement.Integration;

public sealed class PurchaseRequisitionRequestedHandler(ProcurementService procurementService) : IIntegrationEventHandler
{
    public string EventType => "PurchaseRequisitionRequested";

    public async Task HandleAsync(IntegrationEvent integrationEvent, CancellationToken cancellationToken = default)
    {
        using var doc = JsonDocument.Parse(integrationEvent.PayloadJson);
        var root = doc.RootElement;
        var signalId = root.GetProperty("SignalId").GetGuid();
        var itemId = root.GetProperty("ItemId").GetGuid();
        var storeId = root.GetProperty("StoreId").GetGuid();
        var qty = root.GetProperty("SuggestedQty").GetDecimal();
        var sku = root.TryGetProperty("Sku", out var skuEl) ? skuEl.GetString() : "ITEM";
        var name = root.TryGetProperty("Name", out var nameEl) ? nameEl.GetString() : "Item";

        var result = await procurementService.CreateRequisitionFromSignalAsync(
            integrationEvent.FacilityId,
            signalId,
            itemId,
            storeId,
            qty,
            $"Auto PR for {sku} - {name}",
            cancellationToken);

        if (result.IsFailure)
            throw new InvalidOperationException(result.Error);
    }
}
""",
)

w(
    "src/Modules/Procurement/HealthcareERP.Modules.Procurement/DependencyInjection.cs",
    """
using HealthcareERP.BuildingBlocks.Infrastructure.Outbox;
using HealthcareERP.Modules.Procurement.Integration;
using HealthcareERP.Modules.Procurement.Persistence;
using HealthcareERP.Modules.Procurement.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace HealthcareERP.Modules.Procurement;

public static class DependencyInjection
{
    public static IServiceCollection AddProcurementModule(this IServiceCollection services, string? connectionString, bool useInMemory = false)
    {
        if (useInMemory || string.IsNullOrWhiteSpace(connectionString))
            services.AddDbContext<ProcurementDbContext>(o => o.UseInMemoryDatabase("healthcare-erp-prc"));
        else
            services.AddDbContext<ProcurementDbContext>(o => o.UseNpgsql(connectionString));

        services.AddScoped<ProcurementService>();
        services.AddScoped<IIntegrationEventHandler, PurchaseRequisitionRequestedHandler>();
        return services;
    }
}
""",
)

print("module sources written")
