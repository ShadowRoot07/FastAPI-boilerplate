from collections.abc import AsyncGenerator, Callable
from typing import Any
from unittest.mock import AsyncMock, Mock

import pytest
from faker import Faker
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.app.core.config import settings
from src.app.main import app

# Usamos el prefijo ASYNC para los tests
DATABASE_URI = settings.POSTGRES_URI
DATABASE_PREFIX = settings.POSTGRES_ASYNC_PREFIX
async_engine = create_async_engine(DATABASE_PREFIX + DATABASE_URI)
async_session_factory = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

fake = Faker()

@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, Any]:
    # Actualizado a AsyncClient para soportar la naturaleza asíncrona de la app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as _client:
        yield _client
    app.dependency_overrides = {}
    await async_engine.dispose()

@pytest.fixture
async def db() -> AsyncGenerator[AsyncSession, Any]:
    # Fixture de base de datos ahora es asíncrona
    async with async_session_factory() as session:
        yield session
        await session.close()

def override_dependency(dependency: Callable[..., Any], mocked_response: Any) -> None:
    app.dependency_overrides[dependency] = lambda: mocked_response

@pytest.fixture
def mock_db():
    """Mock database session for unit tests."""
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
def mock_redis():
    """Mock Redis connection for unit tests."""
    mock_redis = Mock()
    mock_redis.get = AsyncMock(return_value=None)
    mock_redis.set = AsyncMock(return_value=True)
    mock_redis.delete = AsyncMock(return_value=True)
    return mock_redis

@pytest.fixture
def sample_user_data():
    """Generate sample user data for tests."""
    return {
        "name": fake.name(),
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(),
    }

@pytest.fixture
def sample_user_read():
    """Generate a sample UserRead object."""
    from uuid6 import uuid7
    from src.app.schemas.user import UserRead

    return UserRead(
        id=1,
        uuid=uuid7(),
        name=fake.name(),
        username=fake.user_name(),
        email=fake.email(),
        profile_image_url=fake.image_url(),
        is_superuser=False,
        created_at=fake.date_time(),
        updated_at=fake.date_time(),
        tier_id=None,
    )

@pytest.fixture
def current_user_dict():
    """Mock current user from auth dependency."""
    return {
        "id": 1,
        "username": fake.user_name(),
        "email": fake.email(),
        "name": fake.name(),
        "is_superuser": False,
    }

