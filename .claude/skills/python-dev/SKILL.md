---
name: python-dev
description: Apply python development standards, python-dev. Use when working on python codebase or similar projects.
user-invocable: true
---


## When to Use
Claude applies this skill when:
- Building FastAPI backend services
- Implementing Celery distributed tasks
- Writing database models with SQLAlchemy
- Creating API endpoints with authentication
- Processing asynchronous AI/ML workloads
- Managing web scraping and data collection
- Writing comprehensive unit and integration tests

## Architecture Overview

### Backend Stack (sylia-backend)
- FastAPI with async/await patterns
- SQLAlchemy 2.0 ORM with PostgreSQL
- JWT authentication with Bcrypt password hashing
- Pydantic for data validation and serialization
- Alembic for database migrations
- Domain-Driven Design (DDD) architecture
- Repository pattern with dependency injection
- Comprehensive pytest test suite

### Worker Stack (sylia-celery-workers)
- Celery 5.x distributed task queue
- Redis for message broker and result backend
- OpenAI integration (GPT-5, GPT-4o, DALL-E 3)
- Google Gemini 2.0 Flash integration
- Playwright for browser automation
- BeautifulSoup4 for web scraping
- MinIO for S3-compatible object storage

## Coding Standards

### FastAPI Service Pattern

**Domain Structure** (Repository + Service + API):
```python
# models.py - SQLAlchemy ORM
from app.infrastructure.db import Base
from sqlalchemy import Column, String, DateTime, UUID
from sqlalchemy.orm import relationship
import uuid

class Brand(Base):
    __tablename__ = "brands"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="brands")


# schemas.py - Pydantic validation
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BrandCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    website_url: Optional[str] = None

class BrandSchema(BaseModel):
    id: str
    name: str
    slug: str
    user_id: str
    created_at: datetime

    model_config = {"from_attributes": True}


# service.py - Business logic with repository pattern
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

class BrandRepositoryInterface(ABC):
    @abstractmethod
    async def create_brand(self, brand: BrandSchema) -> BrandSchema:
        pass

    @abstractmethod
    async def get_brand_by_id(self, brand_id: str) -> Optional[BrandSchema]:
        pass

class PostgreSQLBrandRepository(BrandRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    async def create_brand(self, brand: BrandSchema) -> BrandSchema:
        db_brand = BrandModel(**brand.model_dump())
        self.db.add(db_brand)
        self.db.commit()
        self.db.refresh(db_brand)
        return self._model_to_schema(db_brand)

    def _model_to_schema(self, model: BrandModel) -> BrandSchema:
        return BrandSchema(
            id=str(model.id),
            name=model.name,
            slug=model.slug,
            user_id=str(model.user_id),
            created_at=model.created_at
        )

class BrandService:
    def __init__(self, brand_repository: BrandRepositoryInterface):
        self.brand_repository = brand_repository

    async def create_brand(self, brand_data: BrandCreate, user_id: str) -> BrandSchema:
        # Generate slug
        slug = brand_data.name.lower().replace(' ', '-')
        slug = re.sub(r'[^a-z0-9-]', '', slug)

        brand = BrandSchema(
            id=str(uuid.uuid4()),
            name=brand_data.name,
            slug=slug,
            user_id=user_id,
            created_at=datetime.utcnow()
        )
        return await self.brand_repository.create_brand(brand)


# api.py - FastAPI routes
from fastapi import APIRouter, Depends, HTTPException, status
from domains.auth.service import get_current_active_user
from domains.user.models import User

router = APIRouter(prefix="/brands", tags=["brand"])

def get_brand_repository(db: Session = Depends(get_db)) -> BrandRepositoryInterface:
    return PostgreSQLBrandRepository(db)

def get_brand_service(
    repository: BrandRepositoryInterface = Depends(get_brand_repository)
) -> BrandService:
    return BrandService(repository)

@router.post("/", response_model=BrandSchema, status_code=status.HTTP_201_CREATED)
async def create_brand(
    brand_data: BrandCreate,
    current_user: User = Depends(get_current_active_user),
    brand_service: BrandService = Depends(get_brand_service)
):
    """Create a new brand for the authenticated user."""
    return await brand_service.create_brand(brand_data, current_user.id)

@router.get("/{brand_id}", response_model=BrandSchema)
async def get_brand(
    brand_id: str,
    current_user: User = Depends(get_current_active_user),
    brand_service: BrandService = Depends(get_brand_service)
):
    """Get a specific brand by ID."""
    brand = await brand_service.get_brand_by_id(brand_id)

    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found"
        )

    if brand.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this brand"
        )

    return brand
```

### Celery Task Pattern

```python
# tasks/generate.py
from celery import shared_task
from app.config.constants import MAX_RETRIES
import logging

logger = logging.getLogger(__name__)

@shared_task(
    name="app.tasks.generate.generate_text",
    bind=True,
    max_retries=MAX_RETRIES
)
def generate_text(self, prompt: str, max_tokens: int = 1000) -> dict:
    """
    Generate text using OpenAI GPT-5 with structured output.

    Args:
        prompt: The text generation prompt
        max_tokens: Maximum tokens to generate

    Returns:
        dict: {
            "status": "success",
            "data": str,
            "model": str,
            "tokens_in": int,
            "tokens_out": int,
            "tokens_total": int
        }
    """
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Call GPT-5 with Responses API
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7
        )

        result = {
            "status": "success",
            "data": response.choices[0].message.content,
            "model": response.model,
            "tokens_in": response.usage.prompt_tokens,
            "tokens_out": response.usage.completion_tokens,
            "tokens_total": response.usage.total_tokens
        }

        logger.info(f"Text generation completed: {result['tokens_total']} tokens")
        return result

    except Exception as exc:
        logger.exception(f"Error in text generation: {exc}")
        raise self.retry(exc=exc, countdown=60)
```

### Authentication Pattern

```python
# domains/auth/service.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

class TokenService:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def verify_token(self, token: str) -> Optional[TokenData]:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return TokenData(user_id=user_id)
        except JWTError:
            return None

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    token_service = TokenService()
    token_data = token_service.verify_token(token)

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = db.query(UserModel).filter(UserModel.id == token_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

### Database Migration Pattern

```python
# migrations/versions/xxxxx_create_brand_table.py
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade() -> None:
    op.create_table(
        'brands',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_brands_slug'), 'brands', ['slug'], unique=True)

def downgrade() -> None:
    op.drop_index(op.f('ix_brands_slug'), table_name='brands')
    op.drop_table('brands')
```

### Testing Pattern

```python
# test/domains/brand/test_service.py
import pytest
from unittest.mock import AsyncMock
import uuid

class TestBrandService:
    @pytest.fixture
    def mock_repository(self):
        repository = AsyncMock()
        return repository

    @pytest.fixture
    def brand_service(self, mock_repository):
        return BrandService(mock_repository)

    @pytest.fixture
    def sample_brand_create(self):
        return BrandCreate(
            name="Test Brand",
            description="A test brand",
            website_url="https://test.com"
        )

    @pytest.mark.unit
    async def test_create_brand_success(self, brand_service, mock_repository, sample_brand_create):
        user_id = str(uuid.uuid4())
        expected_brand = BrandSchema(
            id=str(uuid.uuid4()),
            name="Test Brand",
            slug="test-brand",
            user_id=user_id,
            created_at=datetime.utcnow()
        )

        mock_repository.create_brand.return_value = expected_brand

        result = await brand_service.create_brand(sample_brand_create, user_id)

        assert result.name == "Test Brand"
        assert result.slug == "test-brand"
        mock_repository.create_brand.assert_called_once()

    @pytest.mark.unit
    async def test_get_brand_by_id_not_found(self, brand_service, mock_repository):
        mock_repository.get_brand_by_id.return_value = None

        result = await brand_service.get_brand_by_id(str(uuid.uuid4()))

        assert result is None
```

### Python Conventions
- Use type hints for all function parameters and return values
- Use `async def` for all service methods and API endpoints
- Use `snake_case` for variables and functions
- Use `PascalCase` for classes
- Keep functions focused and small
- Use early returns to reduce nesting
- Write self-documenting code with clear names
- Use list comprehensions for simple transformations
- Prefer `pathlib` over `os.path` for file operations

### Code Organization Best Practices
- Group related functionality in domain modules
- Separate database models, schemas, services, and API routes
- Use repository pattern for data access abstraction
- Implement dependency injection via FastAPI's Depends
- Keep business logic in service layer, not in routes
- Use Pydantic for all request/response validation
- Store sensitive configuration in environment variables

## Code Organization

### Backend Structure
```
sylia-backend/
├── api/                      # API route aggregation
│   ├── v1.py                # Main v1 router
│   ├── setup.py             # System initialization
│   └── dev.py               # Development routes (DO NOT DEPLOY)
│
├── app/                      # Core application
│   ├── bootstrap.py         # Model auto-loading for Alembic
│   ├── infrastructure/      # Infrastructure layer
│   │   ├── db.py           # Database session
│   │   ├── celery_client.py # Celery integration
│   │   ├── redistool.py    # Redis client
│   │   └── secrets.py      # Encryption utilities
│   └── utils/               # Utility modules
│       ├── Ai.py           # AI wrapper
│       ├── Prompt.py       # Prompt construction
│       └── webscraper.py   # Web scraping
│
├── domains/                  # Domain modules (17 total)
│   ├── auth/                # Authentication
│   ├── brand/               # Brand management
│   ├── user/                # User management
│   ├── color/               # Color management
│   ├── promptvault/         # Prompt templates
│   ├── crawler/             # Web crawling
│   ├── generate/            # Generation API
│   └── shared/              # Shared utilities
│       └── events.py       # Event registry
│
├── migrations/               # Alembic migrations
│   ├── env.py
│   └── versions/            # 20+ migration files
│
├── test/                     # Test suite (52+ files)
│   ├── api/
│   ├── app/
│   └── domains/
│
├── main.py                   # FastAPI entrypoint
├── alembic.ini              # Migration config
├── requirements.txt         # Dependencies
└── pytest.ini               # Test configuration
```

### Worker Structure
```
sylia-celery-workers/
├── app/
│   ├── celery_app.py        # Celery application
│   ├── settings.py          # Environment settings
│   │
│   ├── config/              # Configuration
│   │   ├── celery.py       # Celery config
│   │   ├── constants.py    # Application constants
│   │   └── logging.py      # Logging setup
│   │
│   ├── tasks/               # Task definitions (8 modules)
│   │   ├── generate.py     # GPT-5 text generation
│   │   ├── analyse.py      # GPT-4o image analysis
│   │   ├── gemini.py       # Gemini integration
│   │   ├── dalle.py        # DALL-E image generation
│   │   ├── crawler.py      # Web scraping & screenshots
│   │   ├── initsylia.py    # Website initialization
│   │   ├── images.py       # Image processing
│   │   └── emails.py       # Email notifications
│   │
│   └── utils/               # Utilities
│       ├── storage.py      # MinIO client (479 lines)
│       ├── webscrape.py    # Web crawler (532 lines)
│       ├── seo.py          # SEO analysis (410 lines)
│       └── promptvault.py  # Template management (226 lines)
│
├── tests/
│   ├── conftest.py
│   └── test_tasks.py
│
├── docker/
│   ├── worker.Dockerfile
│   └── compose.yml
│
└── requirements.txt
```

## Key Patterns

### Domain-Driven Design
Each domain follows a consistent structure:
- **models.py** - SQLAlchemy ORM models
- **schemas.py** - Pydantic validation schemas
- **service.py** - Business logic + repository pattern
- **api.py** - FastAPI route definitions
- **events.py** - Domain event handlers (optional)

### Repository Pattern
```python
# Abstract interface
class RepositoryInterface(ABC):
    @abstractmethod
    async def create(self, entity: Schema) -> Schema:
        pass

# Concrete implementation
class PostgreSQLRepository(RepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    async def create(self, entity: Schema) -> Schema:
        # Implementation
        pass

# Dependency injection
def get_repository(db: Session = Depends(get_db)) -> RepositoryInterface:
    return PostgreSQLRepository(db)
```

### Service Layer
```python
class Service:
    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    async def business_operation(self, data: CreateSchema, user_id: str) -> Schema:
        # Business logic here
        result = await self.repository.create(entity)
        # Trigger events, send notifications, etc.
        return result
```

### Async Patterns
- All service methods use `async def`
- All API endpoints use `async def`
- Database operations await results for consistency
- Celery tasks dispatch asynchronously via `send_task()`

### Error Handling
```python
# Service layer returns None for not found
async def get_by_id(self, id: str) -> Optional[Schema]:
    result = await self.repository.get_by_id(id)
    return result  # None if not found

# API layer raises HTTPException
@router.get("/{id}")
async def get_item(id: str, service: Service = Depends(get_service)):
    item = await service.get_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

## Best Practices

### Backend Development
- Use Domain-Driven Design for clear separation of concerns
- Implement repository pattern for testable data access
- Leverage FastAPI's dependency injection system
- Write async-first code throughout the stack
- Use Pydantic for all validation and serialization
- Keep business logic in service layer, not routes
- Implement proper authentication and authorization
- Use UUID primary keys, not auto-increment integers
- Add proper database indexes for query performance
- Write comprehensive tests with pytest markers

### Worker Development
- Define tasks with `@shared_task` decorator
- Use fully qualified task names: `app.tasks.module.function`
- Implement retry logic with exponential backoff
- Log all task execution with structured logging
- Return standardized response dictionaries
- Initialize external clients once per module
- Use environment variables for configuration
- Implement health checks for monitoring
- Store generated assets in MinIO/S3

### Testing
- Write unit tests for service methods
- Write integration tests for repositories
- Write API tests for endpoints
- Use pytest markers: `@pytest.mark.unit`, `@pytest.mark.integration`
- Mock external dependencies (AI services, storage)
- Use fixtures for test data and mock objects
- Test error cases and edge conditions
- Aim for high coverage across all layers

### Database
- Use Alembic for all schema changes
- Write reversible migrations with `upgrade()` and `downgrade()`
- Use `server_default` for timestamps and defaults
- Add foreign key constraints with proper `ondelete` behavior
- Create indexes for frequently queried columns
- Use JSONB for structured JSON data
- Use ARRAY columns for lists when appropriate
- Avoid N+1 queries with proper relationship loading

### Security
- Hash passwords with Bcrypt (never store plain text)
- Use JWT tokens with expiration
- Implement token revocation in database
- Validate ownership before allowing operations
- Use HTTPS in production (TLS termination)
- Implement domain whitelist middleware
- Encrypt sensitive data with Fernet
- Never expose internal IDs or implementation details
- Validate all user input with Pydantic schemas
- Use parameterized queries (SQLAlchemy ORM)
