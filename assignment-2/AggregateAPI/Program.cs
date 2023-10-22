using System.Globalization;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.OpenApi;

var builder = WebApplication.CreateBuilder(args);

int id = Int32.Parse(args[1]);

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var ports = new[] {"5001", "5002", "5003", "5004"};
foreach (var port in ports)
{
    if (("500" + id) == port)
    {
        continue;
    }

    var httpClientName = $"ExternalApi{port}";

    builder.Services.AddHttpClient(httpClientName, client =>
    {
        client.BaseAddress = new Uri($"https://localhost:{port}");
        // You can add additional configuration for each HttpClient if needed.
    });
}

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

int s = -1;
Secrets? scrts = null;

app.MapGet("/", () => "Hello World!");

app.MapPost("/id/{n}", (int n) => 
{
    if (id is null) 
    {
        // parse string n to int
        id = n;
    }

    

    return id;
}).WithOpenApi();

app.MapGet("/id", () => id );

app.MapGet("/deal", () => 
{
    if (s != -1)
    {
        return scrts;
    }

    var random = new Random();
    var max = 2048;
    s = random.Next(1, max);

    var s1 = random.Next(1, max);
    var s2 = random.Next(1, max);
    var s3 = s + max - ((s1 + s2) % max);

    scrts = new Secrets(s1, s2, s3);

    return scrts;
}).WithOpenApi();;

app.MapGet("/admin", () => s);

app.UseHttpsRedirection();

app.Run();

internal record Secrets(int s1, int s2, int s3);
