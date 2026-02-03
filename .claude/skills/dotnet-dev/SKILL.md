---
name: dotnet-dev
description: Apply .NET development best practices and clean architecture patterns. Use when working with C# projects, .NET 8+, ASP.NET Core Web APIs, Entity Framework Core, Blazor applications, or any .NET ecosystem development.
user-invocable: true
---

## When to Use
Claude applies this skill when:
- Building ASP.NET Core Web APIs (REST or minimal APIs)
- Working with Entity Framework Core for data access
- Implementing Clean Architecture or CQRS patterns
- Creating Blazor applications (Server or WebAssembly)
- Writing C# classes, interfaces, and services
- Configuring dependency injection containers
- Implementing authentication and authorization
- Writing unit tests with xUnit or NUnit
- Managing NuGet packages and project dependencies
- Working with appsettings.json configuration
- Implementing background services or hosted services

## Architecture Overview

### Technology Stack
- **.NET 8+** (or latest LTS version)
- **ASP.NET Core** for web APIs and applications
- **Entity Framework Core** for ORM and database access
- **xUnit** or **NUnit** for unit testing
- **FluentValidation** for input validation
- **MediatR** for CQRS and mediator pattern
- **Serilog** or **NLog** for structured logging
- **AutoMapper** for object mapping (use sparingly)

### Clean Architecture Layers
```
Solution/
├── src/
│   ├── Domain/              # Enterprise business rules
│   │   ├── Entities/        # Domain entities
│   │   ├── ValueObjects/    # Value objects
│   │   ├── Enums/           # Enumerations
│   │   └── Exceptions/      # Domain exceptions
│   ├── Application/         # Application business rules
│   │   ├── Common/
│   │   │   ├── Interfaces/  # Repository interfaces, service contracts
│   │   │   ├── Behaviors/   # MediatR pipeline behaviors
│   │   │   └── Mappings/    # AutoMapper profiles
│   │   ├── Features/        # Feature-based organization
│   │   │   ├── Users/
│   │   │   │   ├── Commands/
│   │   │   │   ├── Queries/
│   │   │   │   └── DTOs/
│   │   │   └── Products/
│   │   └── DependencyInjection.cs
│   ├── Infrastructure/      # External concerns
│   │   ├── Persistence/     # EF Core DbContext, configurations
│   │   ├── Identity/        # Authentication/authorization
│   │   ├── Services/        # External service implementations
│   │   └── DependencyInjection.cs
│   └── WebApi/              # Presentation layer
│       ├── Controllers/     # API controllers
│       ├── Middleware/      # Custom middleware
│       ├── Filters/         # Action filters
│       └── Program.cs       # Application entry point
└── tests/
    ├── Domain.UnitTests/
    ├── Application.UnitTests/
    └── WebApi.IntegrationTests/
```

## Coding Standards

### Naming Conventions
```csharp
// Classes, interfaces, methods, properties: PascalCase
public class UserService { }
public interface IUserRepository { }
public string FirstName { get; set; }
public async Task<User> GetUserAsync(int id) { }

// Private fields: _camelCase with underscore prefix
private readonly IUserRepository _userRepository;

// Local variables, parameters: camelCase
public void ProcessUser(int userId)
{
    var userName = GetUserName(userId);
    string fullName = $"{firstName} {lastName}";
}

// Constants: PascalCase
public const int MaxRetryAttempts = 3;

// Avoid Hungarian notation
// ❌ Bad: strUserName, intCount
// ✅ Good: userName, count
```

### Modern C# Features

#### Nullable Reference Types (Always Enable)
```csharp
// Enable in .csproj
<PropertyGroup>
  <Nullable>enable</Nullable>
</PropertyGroup>

// Use nullable annotations properly
public class User
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;  // Non-nullable
    public string? Email { get; set; }                 // Nullable
    public DateTime? LastLoginDate { get; set; }       // Nullable value type
}

// Null checking with pattern matching
if (user?.Email is string email)
{
    SendEmail(email);
}
```

#### Record Types for DTOs and Value Objects
```csharp
// Immutable DTOs with records
public record UserDto(int Id, string Name, string Email);

// Value objects
public record Address(string Street, string City, string ZipCode);

// Records with validation
public record CreateUserRequest
{
    public required string Name { get; init; }
    public required string Email { get; init; }
    public string? PhoneNumber { get; init; }
}
```

#### Primary Constructors (.NET 8+)
```csharp
// Service with primary constructor
public class UserService(
    IUserRepository userRepository,
    ILogger<UserService> logger) : IUserService
{
    public async Task<User?> GetUserAsync(int id)
    {
        logger.LogInformation("Fetching user with ID: {UserId}", id);
        return await userRepository.GetByIdAsync(id);
    }
}
```

#### File-Scoped Namespaces
```csharp
// Use file-scoped namespaces (one less indentation level)
namespace MyApp.Services;

public class UserService
{
    // Implementation
}
```

#### Required Members
```csharp
public class CreateUserCommand
{
    public required string Name { get; init; }
    public required string Email { get; init; }
}
```

### Async/Await Best Practices
```csharp
// Always use async/await for I/O-bound operations
public async Task<User> GetUserAsync(int id, CancellationToken cancellationToken = default)
{
    // Use ConfigureAwait(false) in library code to avoid deadlocks
    var user = await _dbContext.Users
        .FirstOrDefaultAsync(u => u.Id == id, cancellationToken)
        .ConfigureAwait(false);

    return user ?? throw new NotFoundException(nameof(User), id);
}

// Don't mix async and sync code
// ❌ Bad: async void
public async void ProcessUser() { }  // Only for event handlers

// ✅ Good: Return Task
public async Task ProcessUserAsync() { }

// Use ValueTask for hot paths with possible sync completion
public ValueTask<User?> GetCachedUserAsync(int id)
{
    if (_cache.TryGetValue(id, out var user))
        return new ValueTask<User?>(user);

    return new ValueTask<User?>(LoadUserAsync(id));
}
```

### LINQ Best Practices
```csharp
// Use method syntax for simple queries
var activeUsers = users.Where(u => u.IsActive).ToList();

// Use query syntax for complex queries with multiple operations
var result = from user in users
             join order in orders on user.Id equals order.UserId
             where user.IsActive && order.Total > 100
             select new { user.Name, order.Total };

// Avoid multiple enumerations
// ❌ Bad
if (users.Any())
{
    var count = users.Count();  // Enumerated twice
}

// ✅ Good
var userList = users.ToList();
if (userList.Any())
{
    var count = userList.Count;
}

// Use SingleOrDefault when expecting one result
var user = users.SingleOrDefault(u => u.Email == email);

// Use FirstOrDefault when selecting first from many
var latestOrder = orders.OrderByDescending(o => o.Date).FirstOrDefault();
```

## ASP.NET Core Web API Patterns

### Minimal API (Recommended for Simple APIs)
```csharp
// Program.cs with minimal APIs
var builder = WebApplication.CreateBuilder(args);

// Configure services
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));

var app = builder.Build();

// Configure middleware
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthentication();
app.UseAuthorization();

// Define endpoints
app.MapGet("/api/users", async (AppDbContext db) =>
    await db.Users.ToListAsync())
    .WithName("GetUsers")
    .WithOpenApi();

app.MapGet("/api/users/{id:int}", async (int id, AppDbContext db) =>
    await db.Users.FindAsync(id) is User user
        ? Results.Ok(user)
        : Results.NotFound())
    .WithName("GetUser")
    .WithOpenApi();

app.MapPost("/api/users", async (CreateUserRequest request, AppDbContext db) =>
{
    var user = new User { Name = request.Name, Email = request.Email };
    db.Users.Add(user);
    await db.SaveChangesAsync();
    return Results.Created($"/api/users/{user.Id}", user);
})
.WithName("CreateUser")
.WithOpenApi();

app.Run();
```

### Controller-Based API (For Complex APIs)
```csharp
[ApiController]
[Route("api/[controller]")]
public class UsersController(IMediator mediator, ILogger<UsersController> logger) : ControllerBase
{
    [HttpGet]
    [ProducesResponseType(StatusCodes.Status200OK)]
    public async Task<ActionResult<IEnumerable<UserDto>>> GetUsers(
        CancellationToken cancellationToken)
    {
        var query = new GetUsersQuery();
        var result = await mediator.Send(query, cancellationToken);
        return Ok(result);
    }

    [HttpGet("{id:int}")]
    [ProducesResponseType(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<UserDto>> GetUser(
        int id,
        CancellationToken cancellationToken)
    {
        var query = new GetUserByIdQuery(id);
        var result = await mediator.Send(query, cancellationToken);
        return result is not null ? Ok(result) : NotFound();
    }

    [HttpPost]
    [ProducesResponseType(StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<UserDto>> CreateUser(
        [FromBody] CreateUserCommand command,
        CancellationToken cancellationToken)
    {
        var result = await mediator.Send(command, cancellationToken);
        return CreatedAtAction(nameof(GetUser), new { id = result.Id }, result);
    }

    [HttpPut("{id:int}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> UpdateUser(
        int id,
        [FromBody] UpdateUserCommand command,
        CancellationToken cancellationToken)
    {
        if (id != command.Id)
            return BadRequest("ID mismatch");

        await mediator.Send(command, cancellationToken);
        return NoContent();
    }

    [HttpDelete("{id:int}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> DeleteUser(
        int id,
        CancellationToken cancellationToken)
    {
        var command = new DeleteUserCommand(id);
        await mediator.Send(command, cancellationToken);
        return NoContent();
    }
}
```

### CQRS Pattern with MediatR

#### Command Handler
```csharp
// Command
public record CreateUserCommand(string Name, string Email) : IRequest<UserDto>;

// Command Handler
public class CreateUserCommandHandler(
    IApplicationDbContext context,
    ILogger<CreateUserCommandHandler> logger)
    : IRequestHandler<CreateUserCommand, UserDto>
{
    public async Task<UserDto> Handle(
        CreateUserCommand request,
        CancellationToken cancellationToken)
    {
        logger.LogInformation("Creating user with email: {Email}", request.Email);

        var user = new User
        {
            Name = request.Name,
            Email = request.Email,
            CreatedAt = DateTime.UtcNow
        };

        context.Users.Add(user);
        await context.SaveChangesAsync(cancellationToken);

        logger.LogInformation("User created with ID: {UserId}", user.Id);

        return new UserDto(user.Id, user.Name, user.Email);
    }
}
```

#### Query Handler
```csharp
// Query
public record GetUserByIdQuery(int Id) : IRequest<UserDto?>;

// Query Handler
public class GetUserByIdQueryHandler(IApplicationDbContext context)
    : IRequestHandler<GetUserByIdQuery, UserDto?>
{
    public async Task<UserDto?> Handle(
        GetUserByIdQuery request,
        CancellationToken cancellationToken)
    {
        var user = await context.Users
            .AsNoTracking()
            .FirstOrDefaultAsync(u => u.Id == request.Id, cancellationToken);

        return user is not null
            ? new UserDto(user.Id, user.Name, user.Email)
            : null;
    }
}
```

#### Validation Behavior
```csharp
public class ValidationBehavior<TRequest, TResponse>(IEnumerable<IValidator<TRequest>> validators)
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        if (!validators.Any())
            return await next();

        var context = new ValidationContext<TRequest>(request);

        var validationResults = await Task.WhenAll(
            validators.Select(v => v.ValidateAsync(context, cancellationToken)));

        var failures = validationResults
            .SelectMany(r => r.Errors)
            .Where(f => f != null)
            .ToList();

        if (failures.Any())
            throw new ValidationException(failures);

        return await next();
    }
}
```

## Entity Framework Core Best Practices

### DbContext Configuration
```csharp
public class ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
    : DbContext(options), IApplicationDbContext
{
    public DbSet<User> Users => Set<User>();
    public DbSet<Order> Orders => Set<Order>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Apply all configurations from current assembly
        modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
    }

    public override async Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        // Automatically set audit fields
        foreach (var entry in ChangeTracker.Entries<IAuditableEntity>())
        {
            switch (entry.State)
            {
                case EntityState.Added:
                    entry.Entity.CreatedAt = DateTime.UtcNow;
                    break;
                case EntityState.Modified:
                    entry.Entity.UpdatedAt = DateTime.UtcNow;
                    break;
            }
        }

        return await base.SaveChangesAsync(cancellationToken);
    }
}
```

### Entity Configuration (Fluent API)
```csharp
public class UserConfiguration : IEntityTypeConfiguration<User>
{
    public void Configure(EntityTypeBuilder<User> builder)
    {
        builder.ToTable("Users");

        builder.HasKey(u => u.Id);

        builder.Property(u => u.Name)
            .IsRequired()
            .HasMaxLength(100);

        builder.Property(u => u.Email)
            .IsRequired()
            .HasMaxLength(255);

        builder.HasIndex(u => u.Email)
            .IsUnique();

        // Owned entity for value object
        builder.OwnsOne(u => u.Address, address =>
        {
            address.Property(a => a.Street).HasMaxLength(200);
            address.Property(a => a.City).HasMaxLength(100);
            address.Property(a => a.ZipCode).HasMaxLength(10);
        });

        // One-to-many relationship
        builder.HasMany(u => u.Orders)
            .WithOne(o => o.User)
            .HasForeignKey(o => o.UserId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}
```

### Repository Pattern (Optional with EF Core)
```csharp
public interface IRepository<T> where T : class
{
    Task<T?> GetByIdAsync(int id, CancellationToken cancellationToken = default);
    Task<IEnumerable<T>> GetAllAsync(CancellationToken cancellationToken = default);
    Task<T> AddAsync(T entity, CancellationToken cancellationToken = default);
    void Update(T entity);
    void Delete(T entity);
}

public class Repository<T>(ApplicationDbContext context) : IRepository<T>
    where T : class
{
    private readonly DbSet<T> _dbSet = context.Set<T>();

    public async Task<T?> GetByIdAsync(int id, CancellationToken cancellationToken = default)
        => await _dbSet.FindAsync(new object[] { id }, cancellationToken);

    public async Task<IEnumerable<T>> GetAllAsync(CancellationToken cancellationToken = default)
        => await _dbSet.ToListAsync(cancellationToken);

    public async Task<T> AddAsync(T entity, CancellationToken cancellationToken = default)
    {
        await _dbSet.AddAsync(entity, cancellationToken);
        return entity;
    }

    public void Update(T entity) => _dbSet.Update(entity);

    public void Delete(T entity) => _dbSet.Remove(entity);
}
```

### Query Optimization
```csharp
// Use AsNoTracking for read-only queries
var users = await context.Users
    .AsNoTracking()
    .Where(u => u.IsActive)
    .ToListAsync(cancellationToken);

// Eager loading with Include
var usersWithOrders = await context.Users
    .Include(u => u.Orders)
    .ThenInclude(o => o.OrderItems)
    .Where(u => u.IsActive)
    .ToListAsync(cancellationToken);

// Projection to avoid loading entire entities
var userDtos = await context.Users
    .Where(u => u.IsActive)
    .Select(u => new UserDto(u.Id, u.Name, u.Email))
    .ToListAsync(cancellationToken);

// Use pagination
var pageSize = 20;
var pageNumber = 1;
var users = await context.Users
    .OrderBy(u => u.Name)
    .Skip((pageNumber - 1) * pageSize)
    .Take(pageSize)
    .ToListAsync(cancellationToken);
```

## Dependency Injection

### Service Registration
```csharp
// Program.cs or DependencyInjection.cs
public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddMediatR(cfg =>
            cfg.RegisterServicesFromAssembly(Assembly.GetExecutingAssembly()));

        services.AddValidatorsFromAssembly(Assembly.GetExecutingAssembly());

        services.AddTransient(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
        services.AddTransient(typeof(IPipelineBehavior<,>), typeof(LoggingBehavior<,>));

        return services;
    }

    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services.AddDbContext<ApplicationDbContext>(options =>
            options.UseNpgsql(
                configuration.GetConnectionString("DefaultConnection"),
                b => b.MigrationsAssembly(typeof(ApplicationDbContext).Assembly.FullName)));

        services.AddScoped<IApplicationDbContext>(provider =>
            provider.GetRequiredService<ApplicationDbContext>());

        services.AddScoped(typeof(IRepository<>), typeof(Repository<>));
        services.AddScoped<IUserRepository, UserRepository>();

        return services;
    }
}

// Service lifetimes:
// Transient: Created each time they're requested
services.AddTransient<IEmailService, EmailService>();

// Scoped: Created once per request
services.AddScoped<IUserService, UserService>();

// Singleton: Created once for the application lifetime
services.AddSingleton<ICacheService, MemoryCacheService>();
```

## Configuration Management

### appsettings.json Structure
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Database=mydb;Username=user;Password=pass"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "Microsoft.EntityFrameworkCore": "Warning"
    }
  },
  "JwtSettings": {
    "SecretKey": "your-secret-key-min-32-characters",
    "Issuer": "YourApp",
    "Audience": "YourAppUsers",
    "ExpirationMinutes": 60
  },
  "EmailSettings": {
    "SmtpServer": "smtp.gmail.com",
    "SmtpPort": 587,
    "SenderEmail": "noreply@yourapp.com",
    "SenderName": "Your App"
  },
  "AllowedHosts": "*"
}
```

### Strongly-Typed Configuration
```csharp
// Configuration class
public class JwtSettings
{
    public const string SectionName = "JwtSettings";

    public required string SecretKey { get; init; }
    public required string Issuer { get; init; }
    public required string Audience { get; init; }
    public int ExpirationMinutes { get; init; } = 60;
}

// Registration in Program.cs
builder.Services.Configure<JwtSettings>(
    builder.Configuration.GetSection(JwtSettings.SectionName));

// Usage in service
public class TokenService(IOptions<JwtSettings> jwtSettings)
{
    private readonly JwtSettings _jwtSettings = jwtSettings.Value;

    public string GenerateToken(User user)
    {
        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_jwtSettings.SecretKey));
        // ... token generation logic
    }
}
```

## Error Handling and Validation

### Global Exception Handling Middleware
```csharp
public class ExceptionHandlingMiddleware(
    RequestDelegate next,
    ILogger<ExceptionHandlingMiddleware> logger)
{
    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await next(context);
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "An unhandled exception occurred");
            await HandleExceptionAsync(context, ex);
        }
    }

    private static async Task HandleExceptionAsync(HttpContext context, Exception exception)
    {
        var response = context.Response;
        response.ContentType = "application/json";

        var problemDetails = exception switch
        {
            ValidationException validationEx => new ProblemDetails
            {
                Status = StatusCodes.Status400BadRequest,
                Title = "Validation Error",
                Detail = string.Join(", ", validationEx.Errors.Select(e => e.ErrorMessage))
            },
            NotFoundException => new ProblemDetails
            {
                Status = StatusCodes.Status404NotFound,
                Title = "Resource Not Found",
                Detail = exception.Message
            },
            UnauthorizedAccessException => new ProblemDetails
            {
                Status = StatusCodes.Status401Unauthorized,
                Title = "Unauthorized",
                Detail = "You are not authorized to perform this action"
            },
            _ => new ProblemDetails
            {
                Status = StatusCodes.Status500InternalServerError,
                Title = "Internal Server Error",
                Detail = "An error occurred while processing your request"
            }
        };

        response.StatusCode = problemDetails.Status ?? 500;
        await response.WriteAsJsonAsync(problemDetails);
    }
}
```

### FluentValidation
```csharp
public class CreateUserCommandValidator : AbstractValidator<CreateUserCommand>
{
    public CreateUserCommandValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Name is required")
            .MaximumLength(100).WithMessage("Name must not exceed 100 characters");

        RuleFor(x => x.Email)
            .NotEmpty().WithMessage("Email is required")
            .EmailAddress().WithMessage("Email is not valid")
            .MaximumLength(255).WithMessage("Email must not exceed 255 characters");

        RuleFor(x => x.Password)
            .NotEmpty().WithMessage("Password is required")
            .MinimumLength(8).WithMessage("Password must be at least 8 characters")
            .Matches(@"[A-Z]").WithMessage("Password must contain at least one uppercase letter")
            .Matches(@"[a-z]").WithMessage("Password must contain at least one lowercase letter")
            .Matches(@"[0-9]").WithMessage("Password must contain at least one number");
    }
}
```

## Testing Standards

### Unit Tests with xUnit
```csharp
public class UserServiceTests
{
    private readonly Mock<IUserRepository> _userRepositoryMock;
    private readonly Mock<ILogger<UserService>> _loggerMock;
    private readonly UserService _sut;

    public UserServiceTests()
    {
        _userRepositoryMock = new Mock<IUserRepository>();
        _loggerMock = new Mock<ILogger<UserService>>();
        _sut = new UserService(_userRepositoryMock.Object, _loggerMock.Object);
    }

    [Fact]
    public async Task GetUserAsync_WithValidId_ReturnsUser()
    {
        // Arrange
        var userId = 1;
        var expectedUser = new User { Id = userId, Name = "Test User" };
        _userRepositoryMock
            .Setup(x => x.GetByIdAsync(userId, default))
            .ReturnsAsync(expectedUser);

        // Act
        var result = await _sut.GetUserAsync(userId);

        // Assert
        Assert.NotNull(result);
        Assert.Equal(expectedUser.Id, result.Id);
        Assert.Equal(expectedUser.Name, result.Name);
    }

    [Fact]
    public async Task GetUserAsync_WithInvalidId_ThrowsNotFoundException()
    {
        // Arrange
        var userId = 999;
        _userRepositoryMock
            .Setup(x => x.GetByIdAsync(userId, default))
            .ReturnsAsync((User?)null);

        // Act & Assert
        await Assert.ThrowsAsync<NotFoundException>(() => _sut.GetUserAsync(userId));
    }

    [Theory]
    [InlineData(1)]
    [InlineData(5)]
    [InlineData(10)]
    public async Task GetUserAsync_WithMultipleIds_ReturnsCorrectUser(int userId)
    {
        // Arrange
        var expectedUser = new User { Id = userId, Name = $"User {userId}" };
        _userRepositoryMock
            .Setup(x => x.GetByIdAsync(userId, default))
            .ReturnsAsync(expectedUser);

        // Act
        var result = await _sut.GetUserAsync(userId);

        // Assert
        Assert.Equal(userId, result.Id);
    }
}
```

### Integration Tests
```csharp
public class UsersControllerIntegrationTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;
    private readonly WebApplicationFactory<Program> _factory;

    public UsersControllerIntegrationTests(WebApplicationFactory<Program> factory)
    {
        _factory = factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureServices(services =>
            {
                // Remove existing DbContext
                var descriptor = services.SingleOrDefault(
                    d => d.ServiceType == typeof(DbContextOptions<ApplicationDbContext>));
                if (descriptor != null)
                    services.Remove(descriptor);

                // Add in-memory database for testing
                services.AddDbContext<ApplicationDbContext>(options =>
                    options.UseInMemoryDatabase("TestDb"));
            });
        });

        _client = _factory.CreateClient();
    }

    [Fact]
    public async Task GetUsers_ReturnsSuccessStatusCode()
    {
        // Act
        var response = await _client.GetAsync("/api/users");

        // Assert
        response.EnsureSuccessStatusCode();
        Assert.Equal("application/json; charset=utf-8",
            response.Content.Headers.ContentType?.ToString());
    }

    [Fact]
    public async Task CreateUser_WithValidData_ReturnsCreatedUser()
    {
        // Arrange
        var newUser = new { Name = "Test User", Email = "test@example.com" };
        var content = new StringContent(
            JsonSerializer.Serialize(newUser),
            Encoding.UTF8,
            "application/json");

        // Act
        var response = await _client.PostAsync("/api/users", content);

        // Assert
        response.EnsureSuccessStatusCode();
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);

        var responseContent = await response.Content.ReadAsStringAsync();
        var createdUser = JsonSerializer.Deserialize<UserDto>(responseContent);
        Assert.NotNull(createdUser);
        Assert.Equal(newUser.Name, createdUser.Name);
    }
}
```

## Authentication & Authorization

### JWT Authentication Setup
```csharp
// Program.cs
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        var jwtSettings = builder.Configuration.GetSection("JwtSettings").Get<JwtSettings>();
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = jwtSettings!.Issuer,
            ValidAudience = jwtSettings.Audience,
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(jwtSettings.SecretKey))
        };
    });

builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("AdminOnly", policy => policy.RequireRole("Admin"));
    options.AddPolicy("UserOrAdmin", policy =>
        policy.RequireRole("User", "Admin"));
});
```

### Authorization in Controllers
```csharp
[Authorize]
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    [AllowAnonymous]
    [HttpPost("register")]
    public async Task<IActionResult> Register(RegisterRequest request)
    {
        // Registration logic
    }

    [AllowAnonymous]
    [HttpPost("login")]
    public async Task<IActionResult> Login(LoginRequest request)
    {
        // Login logic
    }

    [Authorize(Roles = "Admin")]
    [HttpDelete("{id:int}")]
    public async Task<IActionResult> DeleteUser(int id)
    {
        // Only admins can delete users
    }

    [Authorize(Policy = "UserOrAdmin")]
    [HttpGet("{id:int}")]
    public async Task<IActionResult> GetUser(int id)
    {
        // Users and admins can view
    }
}
```

## Logging Best Practices

### Structured Logging with Serilog
```csharp
// Program.cs
using Serilog;

Log.Logger = new LoggerConfiguration()
    .WriteTo.Console()
    .WriteTo.File("logs/log-.txt", rollingInterval: RollingInterval.Day)
    .CreateLogger();

try
{
    var builder = WebApplication.CreateBuilder(args);

    builder.Host.UseSerilog((context, configuration) =>
        configuration.ReadFrom.Configuration(context.Configuration));

    // ... rest of configuration
}
catch (Exception ex)
{
    Log.Fatal(ex, "Application failed to start");
}
finally
{
    Log.CloseAndFlush();
}

// Usage in services
public class UserService(ILogger<UserService> logger)
{
    public async Task<User> CreateUserAsync(CreateUserCommand command)
    {
        logger.LogInformation(
            "Creating user with email: {Email}",
            command.Email);

        try
        {
            // Create user logic
            logger.LogInformation(
                "User created successfully with ID: {UserId}",
                user.Id);
            return user;
        }
        catch (Exception ex)
        {
            logger.LogError(
                ex,
                "Error creating user with email: {Email}",
                command.Email);
            throw;
        }
    }
}
```

## Project File (.csproj) Standards

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <WarningsAsErrors />
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="8.0.0" />
    <PackageReference Include="Npgsql.EntityFrameworkCore.PostgreSQL" Version="8.0.0" />
    <PackageReference Include="MediatR" Version="12.0.0" />
    <PackageReference Include="FluentValidation.DependencyInjectionExtensions" Version="11.9.0" />
    <PackageReference Include="Serilog.AspNetCore" Version="8.0.0" />
    <PackageReference Include="Swashbuckle.AspNetCore" Version="6.5.0" />
  </ItemGroup>

</Project>
```

## Best Practices Summary

### Code Quality
1. **Enable nullable reference types** in all projects
2. **Use primary constructors** for dependency injection (.NET 8+)
3. **Prefer record types** for DTOs and value objects
4. **Use file-scoped namespaces** to reduce indentation
5. **Follow async/await best practices** - always return Task, use ConfigureAwait(false) in libraries
6. **Write LINQ efficiently** - avoid multiple enumerations

### Architecture
1. **Follow Clean Architecture** principles - separate concerns by layer
2. **Use CQRS with MediatR** for complex business logic
3. **Implement repository pattern** only when it adds value (EF Core DbContext is already a repository)
4. **Use dependency injection** properly - understand service lifetimes
5. **Keep controllers thin** - delegate to MediatR handlers or services

### Data Access
1. **Use AsNoTracking** for read-only queries
2. **Eager load with Include** when needed, but prefer projection
3. **Use pagination** for large result sets
4. **Configure entities with Fluent API** in separate configuration classes
5. **Implement proper indexes** on frequently queried columns

### API Design
1. **Use minimal APIs** for simple endpoints, controllers for complex scenarios
2. **Return proper HTTP status codes** (200, 201, 204, 400, 404, 500)
3. **Include ProducesResponseType** attributes for OpenAPI documentation
4. **Version your APIs** when making breaking changes
5. **Accept CancellationToken** in all async methods

### Security
1. **Use JWT for stateless authentication**
2. **Implement proper authorization** with policies and roles
3. **Never store secrets in code** - use configuration and Azure Key Vault
4. **Validate all input** with FluentValidation
5. **Use HTTPS** in production

### Testing
1. **Write unit tests** for business logic and handlers
2. **Use integration tests** for API endpoints
3. **Mock dependencies** with Moq or NSubstitute
4. **Follow AAA pattern** (Arrange, Act, Assert)
5. **Use Theory and InlineData** for parametrized tests

### Error Handling
1. **Implement global exception handling middleware**
2. **Use custom exceptions** (NotFoundException, ValidationException)
3. **Return ProblemDetails** for consistent error responses
4. **Log errors** with appropriate log levels

### Performance
1. **Use ValueTask** for hot paths
2. **Cache frequently accessed data** with IMemoryCache
3. **Use AsNoTracking** for read-only queries
4. **Implement pagination** for large datasets
5. **Profile and optimize** database queries with EF Core logging

---

**Last Updated:** February 2026
**Compatible with:** .NET 8+, ASP.NET Core 8+, Entity Framework Core 8+
