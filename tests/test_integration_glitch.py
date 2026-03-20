import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os

@pytest.mark.asyncio
async def test_real_database_connection():
    # Priorizamos variables de entorno reales del sistema
    host = os.getenv("POSTGRES_SERVER", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "password123")
    db = os.getenv("POSTGRES_DB", "postgres")
    database_url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
    
    # Esto saldrá en los logs de GitHub si falla
    print(f"\nDEBUG: Intentando conectar a {user}@^{host}:{port}/{db}")
    
    engine = create_async_engine(database_url)
    
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
            print("\nDEBUG: ¡Conexión exitosa!")
    finally:
        await engine.dispose()

