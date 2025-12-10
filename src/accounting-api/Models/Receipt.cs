using System;
using System.Collections.Generic;

namespace AccountingApi.Models;

public class Receipt
{
    public int? Id { get; set; }
    public Store? Store { get; set; }
    public ReceiptInfo? ReceiptInfo { get; set; }
    public List<Item>? Items { get; set; }
    public Totals? Totals { get; set; }
}

public class Store
{
    public int Id { get; set; }
    public string? Name { get; set; }
    public string? Address { get; set; }
}

public class ReceiptInfo
{
    public int Id { get; set; }
    public string? Date { get; set; }
}

public class Item
{
    public int Id { get; set; }
    public string? Name { get; set; }
    public decimal? Price { get; set; }
}

public class Totals
{
    public int Id { get; set; }
    public decimal? Total { get; set; }
}
