using Microsoft.EntityFrameworkCore;
using AccountingApi.Data;
using AccountingApi.Models;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddOpenApi();
builder.Services.AddSwaggerGen();
builder.Services.AddDbContext<AccountingDbContext>(options =>
    options.UseSqlite("Data Source=accounting.db"));

var app = builder.Build();

// Create database and seed data
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AccountingDbContext>();
    db.Database.EnsureCreated();

    // Seed data if empty
    if (!db.Invoices.Any())
    {
        var invoices = new[]
        {
            new Receipt
            {
                Store = new Store { Name = "Billa AG", Address = "3400 KLOSTERNEUBURG, AUFELDGASSE 45-49" },
                ReceiptInfo = new ReceiptInfo { Date = "2025-07-25" },
                Items = new List<Item>
                {
                    new Item { Name = "Billa Bio Zitronen 500g", Price = 2.49m },
                    new Item { Name = "Ja! Bio Knoblauch 150g", Price = 2.99m },
                    new Item { Name = "Ja!Bio RoggenPurWeck", Price = 1.09m },
                    new Item { Name = "Ja! Bio Wachauer", Price = 1.35m }
                },
                Totals = new Totals { Total = 7.92m }
            },
            new Receipt
            {
                Store = new Store { Name = "SPAR", Address = "1010 WIEN, STEPHANSPLATZ 3" },
                ReceiptInfo = new ReceiptInfo { Date = "2025-07-26" },
                Items = new List<Item>
                {
                    new Item { Name = "SPAR Milch 1L", Price = 1.29m },
                    new Item { Name = "SPAR Brot 500g", Price = 2.49m },
                    new Item { Name = "SPAR Butter 250g", Price = 3.99m },
                    new Item { Name = "SPAR Käse 150g", Price = 2.79m }
                },
                Totals = new Totals { Total = 10.56m }
            }
        };

        db.Invoices.AddRange(invoices);
        db.SaveChanges();
    }
}

// Configure the HTTP request pipeline.
app.MapOpenApi();
app.UseSwagger();
app.UseSwaggerUI(options =>
{
    options.RoutePrefix = string.Empty; // Swagger UI at root /
    options.SwaggerEndpoint("/openapi/v1.json", "accounting-api v1");
});

// Receipt endpoints
app.MapPost("/invoices", async (Receipt receipt, AccountingDbContext db) =>
{
    db.Invoices.Add(receipt);
    await db.SaveChangesAsync();
    return Results.Created($"/invoices/{receipt.Id}", receipt);
})
.WithName("AddInvoice")
.WithOpenApi();

app.MapGet("/invoices", async (AccountingDbContext db) =>
{
    return await db.Invoices.ToListAsync();
})
.WithName("GetInvoices")
.WithOpenApi();

app.Run();
