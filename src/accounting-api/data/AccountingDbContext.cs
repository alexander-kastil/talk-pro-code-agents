using Microsoft.EntityFrameworkCore;
using AccountingApi.Models;

namespace AccountingApi.Data;

public class AccountingDbContext : DbContext
{
    public AccountingDbContext(DbContextOptions<AccountingDbContext> options)
        : base(options)
    {
    }

    public DbSet<Receipt> Invoices { get; set; } = null!;

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Configure Receipt as the aggregate root
        modelBuilder.Entity<Receipt>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Id).ValueGeneratedOnAdd();

            // Configure Store as owned type
            entity.OwnsOne(e => e.Store, sa =>
            {
                sa.Property(s => s.Name);
                sa.Property(s => s.Address);
            });

            // Configure ReceiptInfo as owned type
            entity.OwnsOne(e => e.ReceiptInfo, ri =>
            {
                ri.Property(r => r.Date);
            });

            // Configure Totals as owned type
            entity.OwnsOne(e => e.Totals, t =>
            {
                t.Property(tot => tot.Total);
            });

            // Configure Items as owned collection
            entity.OwnsMany(e => e.Items, item =>
            {
                item.Property(i => i.Name);
                item.Property(i => i.Price);
                item.WithOwner().HasForeignKey("ReceiptId");
                item.HasKey("Id");
            });
        });
    }
}
