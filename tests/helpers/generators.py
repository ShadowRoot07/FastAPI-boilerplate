from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import uuid7

from src.app import models
from src.app.core.security import get_password_hash
from tests.conftest import fake

async def create_user(db: AsyncSession, is_super_user: bool = False) -> models.User:
    _user = models.User(
        name=fake.name(),
        username=fake.user_name(),
        email=fake.email(),
        hashed_password=get_password_hash(fake.password()),
        profile_image_url=fake.image_url(),
        uuid=uuid7(), # Se agregaron paréntesis para generar el valor
        is_superuser=is_super_user,
    )

    db.add(_user)
    await db.commit()   # Cambio a commit asíncrono
    await db.refresh(_user) # Cambio a refresh asíncrono

    return _user

