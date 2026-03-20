import pytest
from sqlalchemy.ext.asyncio import create_async_backend
from sqlalchemy import text
import os

@pytest.mark.asyncio
async def test_real_database_connection():
    """
    TEST DE INTEGRACIÓN REAL:
    Este test intenta tocar el Postgres de GitHub Actions.
    Si el boilerplate está mal configurado, este test explotará.
    """
    # Intentamos obtener la URL de conexión del entorno
    host = os.getenv("POSTGRES_SERVER", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    user = "postgres"
    password = "password"
    db = "fastapi_db"
    
    # URL de conexión asíncrona (usando asyncpg)
    database_url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
    
    print(f"\n🚀 Intentando conexión real a: {database_url}")
    
    from sqlalchemy.ext.asyncio import create_async_engine
    engine = create_async_engine(database_url)
    
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        val = result.scalar()
        assert val == 1
        print("✅ ¡CONEXIÓN REAL EXITOSA! El glitch no está en la base de datos.")
    
    await engine.dispose()

