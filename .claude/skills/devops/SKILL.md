---
name: devops
description: Apply devops standards, devops. Use when working on devops in the projects.
user-invocable: true
---

## When to Use
Claude applies this skill when:
- Building or modifying Docker containers
- Working with docker-compose configurations
- Creating or updating Makefiles
- Setting up CI/CD pipelines
- Managing container registry deployments
- Testing APIs with Bruno
- Configuring environment variables
- Managing multi-service architectures
- Deploying to production environments

## Architecture Overview

### Sylia.io Stack
The Sylia.io project uses a microservices architecture with the following components:

#### Core Services
- **sylia-backend**: FastAPI Python backend (port 8000)
- **sylia-frontend**: Vue 3 frontend (port 3050)
- **sylia-postgres**: PostgreSQL 17 database (port 5432)
- **sylia-landlord-backend**: Landlord management API (port 8001)
- **sylia-landlord-frontend**: Landlord Vue 3 frontend (port 3051)

#### Supporting Services
- **sylia-celery-worker**: Background task processing
- **sylia-redis**: Redis cache and Celery broker (port 6379)
- **sylia-minio**: S3-compatible object storage (ports 9000, 9001)
- **sylia-agent**: AI agent service (port 8003)
- **sylia-mcp**: MCP protocol service (port 8002)

#### Container Registry
- **Registry**: `rg.nl-ams.scw.cloud/moonlight-registry`
- **Provider**: Scaleway Container Registry (Amsterdam)

## Makefile Standards

### Modular Makefile Architecture
The project uses a modular Makefile system with the root `Makefile` including specialized modules from `makefiles/`:

```makefile
include makefiles/help.mk
include makefiles/devops.mk
include makefiles/build.mk
include makefiles/setup.mk
include makefiles/ui.mk
include makefiles/magic.mk
include makefiles/clean.mk
```

### Key Makefile Targets

#### Setup Commands (`makefiles/setup.mk`)
```bash
make get-all              # Clone all repositories
make get-frontend         # Clone frontend repository
make get-backend          # Clone backend repository
make get-landlord-backend # Clone landlord backend repository
make get-postgres         # Clone postgres repository
make get-celery          # Clone celery workers repository
make get-workers         # Clone workers repository
make get-website         # Clone website repository
```

#### Build Commands (`makefiles/build.mk`)
```bash
make build-all              # Build all Docker images
make build-frontend         # Build frontend Docker image
make build-backend          # Build backend Docker image
make build-landlord-backend # Build landlord backend Docker image
make build-postgres         # Build postgres Docker image
make run                    # Start all services with docker-compose
make stop                   # Stop all services
```

#### DevOps Commands (`makefiles/devops.mk`)
```bash
make login-registry     # Login to Scaleway Container Registry
make push-image IMAGE=myapp:latest  # Push image to registry
make deploy-frontend    # Build and push frontend to registry
make pull-frontend      # Pull frontend image from registry
```

#### Registry Build Commands (Root `Makefile`)
```bash
# Build and push with auto-derived image name
make build-push CONTEXT=./sylia-backend

# Build and push with version tagging
make build-push-registry CONTEXT=./sylia-backend VERSION=0.0.8

# Build all core services
make build-all
```

**Registry Variables:**
- `REGISTRY`: Container registry URL (default: `rg.nl-ams.scw.cloud/moonlight-registry`)
- `TAG`: Image tag (default: `latest`)
- `VERSION`: Semantic version (auto-derived from git or custom)
- `CONTEXT`: Build context directory (e.g., `./sylia-backend`)
- `DOCKERFILE`: Dockerfile path (default: `$(CONTEXT)/Dockerfile`)

#### Clean Commands (`makefiles/clean.mk`)
```bash
make clean-all              # Remove all project directories
make clean-frontend         # Remove frontend directory
make clean-backend          # Remove backend directory
make clean-landlord-backend # Remove landlord backend directory
make clean-postgres         # Remove postgres directory
make clean-website          # Remove website directory
```

#### UI Commands (`makefiles/ui.mk`)
```bash
make open-all      # Open all service UIs in browser
make open-api      # Open FastAPI backend (http://localhost:8000)
make open-landlord # Open Landlord Frontend
make open-tenant   # Open Tenant Frontend
make open-pgadmin  # Open pgAdmin
make open-redis    # Open Redis Commander
```

### Makefile Conventions
- Use `.PHONY` declarations for non-file targets
- Include ASCII art headers with Sylia.io branding
- Add author attribution: `Author: Vincent Brand, 2025`
- Use `@echo` for user-friendly output messages
- Support cross-platform commands (detect OS with `uname -s`)
- Use `||` for graceful error handling
- Sleep between browser opens (`@sleep 2`) to prevent overload

## Docker Standards

### Dockerfile Best Practices

#### Python/FastAPI Services
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copy and install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Key Points:**
- Use slim base images (`python:3.12-slim`)
- Optimize layer caching (dependencies before code)
- Use `--no-cache-dir` for pip to reduce image size
- Set `WORKDIR /app` consistently
- Expose appropriate ports

#### Node/Vue Services
```dockerfile
FROM node:20-alpine

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache curl

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Build the application
RUN npm run build

EXPOSE 3050

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:3050 || exit 1

# Start application
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "3050"]
```

**Key Points:**
- Use alpine images for smaller size (`node:20-alpine`)
- Install `curl` for healthchecks
- Build application in Dockerfile
- Include comprehensive healthchecks
- Use `--host 0.0.0.0` for Docker networking

#### PostgreSQL Services
```dockerfile
FROM postgres:17-alpine

# Set labels
LABEL maintainer="Vincent Brand <vincent@sylia.io>"
LABEL description="PostgreSQL database for Sylia.io application"
LABEL version="17.0"

# Create custom directories
RUN mkdir -p /docker-entrypoint-initdb.d
RUN mkdir -p /var/lib/postgresql/backup

# Copy configuration files
COPY postgresql.conf /etc/postgresql/postgresql.conf
COPY pg_hba.conf /etc/postgresql/pg_hba.conf

# Copy initialization scripts
COPY init-scripts/ /docker-entrypoint-initdb.d/

# Set proper permissions
RUN chmod -R 755 /docker-entrypoint-initdb.d/
RUN chown -R postgres:postgres /var/lib/postgresql/backup

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD pg_isready -U $POSTGRES_USER -d $POSTGRES_DB || exit 1

EXPOSE 5432
```

**Key Points:**
- Use official PostgreSQL alpine images
- Add maintainer labels
- Create backup directories
- Copy custom configurations
- Set proper file permissions
- Include comprehensive healthchecks

### Docker Compose Standards

#### Service Definition Pattern
```yaml
servicename:
  build:
    context: ./servicename
    dockerfile: Dockerfile
  container_name: servicename
  ports:
    - "8000:8000"
  env_file: .env
  volumes:
    - ./servicename:/app
    - /app/__pycache__
  environment:
    - PYTHONPATH=/app
  restart: unless-stopped
  depends_on:
    dependency:
      condition: service_healthy
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 40s
```

**Key Standards:**
- Use `container_name` for easy identification
- Always include `restart: unless-stopped`
- Use `env_file: .env` for root environment variables
- Mount volumes for development (code + exclude caches)
- Use `depends_on` with `condition: service_healthy`
- Include comprehensive healthchecks
- Use named volumes for persistent data

#### Network Configuration
```yaml
networks:
  default:
    name: sylia-network
```

**Standards:**
- Use custom network names (`sylia-network`)
- Default network for standard services
- Separate networks for isolated services (e.g., `sylia-agent-network`)

#### Volume Management
```yaml
volumes:
  sylia_postgres_data:
    driver: local
  sylia_postgres_backup:
    driver: local
  redis_data:
    driver: local
```

**Standards:**
- Use descriptive volume names with service prefix
- Use `driver: local` explicitly
- Create separate volumes for data and backups

### Healthcheck Standards

**Python/FastAPI:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

**Node/Vue:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:3050 || exit 1
```

**PostgreSQL:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD pg_isready -U $POSTGRES_USER -d $POSTGRES_DB || exit 1
```

**Standards:**
- Use appropriate intervals (30s standard)
- Set longer `start-period` for services that need initialization
- Use 3-5 retries before marking unhealthy
- Use service-specific health check commands

## Bruno API Testing

### Collection Structure
```
bruno/Sylia/
├── bruno.json              # Collection configuration
├── collection.bru          # Collection-level variables
├── development/            # Development environment tests
│   ├── v1/                # API version 1
│   │   ├── auth/          # Authentication endpoints
│   │   ├── brands/        # Brand endpoints
│   │   ├── colors/        # Color endpoints
│   │   ├── settings/      # Settings endpoints
│   │   └── ...
│   ├── core/              # Core API tests
│   ├── db/                # Database operations
│   └── setup/             # Setup scripts
└── test/                  # Test suite
    └── v1/                # Ordered test sequence
        ├── 01 Register User.bru
        ├── 02 Login User.bru
        ├── 03 Get Current User.bru
        └── ...
```

### Collection Configuration
**bruno.json:**
```json
{
  "version": "1",
  "name": "Sylia",
  "type": "collection",
  "ignore": [
    "node_modules",
    ".git"
  ]
}
```

### Collection Variables
**collection.bru:**
```bru
vars:pre-request {
  base_url: http://localhost:8000
  version: /v1
}
```

### Request File Structure
**Example: Login User.bru**
```bru
meta {
  name: Login User
  type: http
  seq: 2
}

post {
  url: {{base_url}}/v1/auth/login
  body: json
  auth: none
}

body:json {
  {
    "email": "demo@sylia.io",
    "password": "DemoPassword123!"
  }
}

script:post-response {
  if (res.getStatus() === 200) {
    bru.setVar("auth_token", res.getBody().access_token);
  }
}

tests {
  test("should login successfully", function() {
    expect(res.getStatus()).to.equal(200);
    expect(res.getBody().access_token).to.be.a("string");
    expect(res.getBody().token_type).to.equal("bearer");
    expect(res.getBody().expires_in).to.be.a("number");
  });
}
```

### Bruno Standards

#### Meta Section
- Use descriptive names
- Set `type: http` for API requests
- Use `seq` for test ordering in test suites

#### Request Configuration
- Use collection variables (`{{base_url}}`, `{{version}}`)
- Set appropriate auth (`none`, `bearer`, etc.)
- Use `body: json` for JSON payloads

#### Pre-request Scripts
```javascript
script:pre-request {
  // Generate dynamic test data
  const suffix = Date.now();
  const prefix = `bruno-${suffix}`;

  bru.setVar("test_email", `bruno+${suffix}@example.com`);
  bru.setVar("test_username", `bruno_user_${suffix}`);
  bru.setVar("test_password", "DemoPassword123!");
}
```

#### Post-response Scripts
```javascript
script:post-response {
  // Store tokens and IDs for subsequent requests
  if (res.getStatus() === 200) {
    bru.setVar("auth_token", res.getBody().access_token);
    bru.setVar("user_id", res.getBody().user.id);
  }
}
```

#### Test Assertions
```javascript
tests {
  test("should return 200 OK", function() {
    expect(res.getStatus()).to.equal(200);
  });

  test("should return valid data structure", function() {
    expect(res.getBody().field).to.be.a("string");
    expect(res.getBody().count).to.be.a("number");
    expect(res.getBody().active).to.equal(true);
  });
}
```

### Test Organization Best Practices
1. **Separate development and test folders**
   - `development/`: Ad-hoc testing and exploration
   - `test/`: Sequential integration test suites

2. **Use numbered prefixes for test sequences**
   - `01 Register User.bru`
   - `02 Login User.bru`
   - `03 Get Current User.bru`

3. **Chain requests with variables**
   - Store auth tokens in post-response scripts
   - Use stored IDs in subsequent requests
   - Clean up test data when needed

4. **Organize by API version and resource**
   - Group endpoints by version (`/v1/`, `/v2/`)
   - Group by resource type (`/auth/`, `/brands/`, `/colors/`)

## Environment Configuration

### Environment File Structure
```bash
# Database Configuration
POSTGRES_DB=sylia_db
POSTGRES_USER=sylia_user
POSTGRES_PASSWORD=sylia_secure_password

# Application Configuration
DATABASE_URL=postgresql://sylia_user:sylia_secure_password@localhost:5432/sylia_db
SECRET_KEY=your-super-secret-key-change-this-in-production

# Environment
NODE_ENV=development
PYTHONPATH=/app

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=true

# Frontend Configuration
FRONTEND_PORT=3050
FRONTEND_HOST=0.0.0.0
```

### Environment Best Practices
1. **Always provide `.env.example`** with safe defaults
2. **Never commit `.env`** to version control (add to `.gitignore`)
3. **Use descriptive variable names** (prefix with service: `POSTGRES_`, `API_`, etc.)
4. **Document required variables** with comments
5. **Use different files for different environments** (`.env.prod`, `.env.dev`)
6. **Reference root `.env` in docker-compose** with `env_file: .env`

## Container Registry & Deployment

### Scaleway Container Registry
**Registry URL:** `rg.nl-ams.scw.cloud/moonlight-registry`

### Login to Registry
```bash
make login-registry
```
Or manually:
```bash
echo "API_KEY" | docker login rg.nl-ams.scw.cloud/moonlight-registry \
  --username scaleway --password-stdin
```

### Build and Push Images

#### Single Service
```bash
# Build and push with latest tag
make build-push CONTEXT=./sylia-backend

# Build and push with version
make build-push-registry CONTEXT=./sylia-backend VERSION=0.0.8
```

#### All Services
```bash
make build-all
```

### Image Naming Convention
- **Pattern:** `registry/servicename:tag`
- **Example:** `rg.nl-ams.scw.cloud/moonlight-registry/sylia-backend:latest`
- **Image name:** Auto-derived from CONTEXT folder name (lowercase)
- **Tags:** Support both `TAG` (latest, dev) and `VERSION` (0.0.8, 1.2.3)

### Deployment Workflow
1. **Build locally:** Test image builds successfully
2. **Login to registry:** `make login-registry`
3. **Build and push:** `make build-push-registry CONTEXT=./service VERSION=x.y.z`
4. **Verify push:** Check Scaleway console
5. **Deploy:** Pull image on production server and restart services

## Service Organization

### Port Allocation
```
5432  - PostgreSQL
6379  - Redis
8000  - sylia-backend (FastAPI)
8001  - sylia-landlord-backend (FastAPI)
8002  - sylia-mcp (MCP Protocol)
8003  - sylia-agent (AI Agent)
9000  - MinIO S3 API
9001  - MinIO Console
3050  - sylia-frontend (Vue 3)
3051  - sylia-landlord-frontend (Vue 3)
```

### Directory Structure
```
Sylia/
├── .claude/                    # Claude Code skills
│   └── skills/
│       ├── devops/
│       └── vue3-dev/
├── bruno/                      # API test collections
│   └── Sylia/
├── makefiles/                  # Modular makefiles
│   ├── help.mk
│   ├── devops.mk
│   ├── build.mk
│   ├── setup.mk
│   ├── ui.mk
│   ├── clean.mk
│   └── magic.mk
├── sylia-backend/             # Python FastAPI backend
├── sylia-frontend/            # Vue 3 frontend
├── sylia-landlord-backend/    # Landlord API
├── sylia-landlord-frontend/   # Landlord UI
├── sylia-postgres/            # PostgreSQL container
├── sylia-celery-workers/      # Celery workers
├── sylia-agent/               # AI agent service
├── sylia-mcp/                 # MCP protocol service
├── Makefile                   # Root makefile
├── docker-compose.yml         # Main services
├── docker-compose.agent.yml   # Agent services
├── .env                       # Environment variables
└── .env.example               # Environment template
```

## Best Practices

### Docker Best Practices
1. **Use multi-stage builds** when needed for production optimization
2. **Minimize layers** by combining RUN commands with `&&`
3. **Order Dockerfile commands** from least to most frequently changing
4. **Use `.dockerignore`** to exclude unnecessary files
5. **Set resource limits** in docker-compose (memory, CPU)
6. **Always include healthchecks** for all services
7. **Use alpine images** when possible for smaller size

### Makefile Best Practices
1. **Use `.PHONY`** for all non-file targets
2. **Document targets** with comments
3. **Keep targets focused** - one responsibility per target
4. **Chain commands** with `&&` for sequential operations
5. **Use `||` for fallback** behavior (e.g., `git clone || git pull`)
6. **Add help targets** for user guidance (`make help`)
7. **Support variables** for flexibility (CONTEXT, TAG, VERSION)

### Bruno Testing Best Practices
1. **Maintain separate environments** (development, production)
2. **Use sequential numbering** for integration tests
3. **Store credentials** in environment variables
4. **Chain requests** using post-response scripts
5. **Write comprehensive assertions** in tests
6. **Generate unique test data** with timestamps
7. **Clean up test data** after test runs

### Security Best Practices
1. **Never commit secrets** to version control
2. **Use strong passwords** in production
3. **Rotate credentials** regularly
4. **Limit exposed ports** in production
5. **Use environment-specific configs** (.env.prod vs .env)
6. **Keep base images updated** with security patches
7. **Use non-root users** in Dockerfiles when possible

### Deployment Best Practices
1. **Tag images with versions** for rollback capability
2. **Test locally** before pushing to registry
3. **Use health checks** to verify deployments
4. **Monitor logs** during deployment
5. **Have rollback plan** ready
6. **Document deployment steps** in README
7. **Use CI/CD pipelines** for automation

## Common Workflows

### New Service Setup
1. Create service directory: `mkdir sylia-newservice`
2. Add Dockerfile following standards
3. Update docker-compose.yml with service definition
4. Add Makefile targets in appropriate module
5. Create Bruno collection for API testing
6. Update .env.example with new variables
7. Test locally: `make build-newservice && make run`
8. Push to registry: `make build-push-registry CONTEXT=./sylia-newservice VERSION=0.1.0`

### Update Existing Service
1. Make code changes
2. Test locally: `docker-compose up --build servicename`
3. Run Bruno tests: Test relevant endpoints
4. Build and push: `make build-push-registry CONTEXT=./service VERSION=x.y.z`
5. Deploy on production: Pull new image and restart

### Debug Service Issues
1. Check logs: `docker-compose logs servicename`
2. Check health: `docker ps` (verify healthy status)
3. Enter container: `docker exec -it servicename /bin/sh`
4. Verify environment: Check env vars inside container
5. Test connectivity: Use Bruno or curl to test endpoints
6. Review docker-compose: Verify depends_on and networks

### Full System Start
1. Ensure `.env` is configured
2. Start core services: `make run` or `docker-compose up -d`
3. Check service health: `docker ps`
4. Verify with Bruno: Run health check tests
5. Open UIs: `make open-all`

---

**Author:** Vincent Brand, 2025
**Project:** Sylia.io
**Last Updated:** January 2026
