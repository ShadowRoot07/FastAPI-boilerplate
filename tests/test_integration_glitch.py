import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os

@pytest.mark.asyncio
async def test_real_database_connection():
    """
    TEST DE INTEGRACIÓN REAL:
    Corregido para usar create_async_engine directamente.
    """
    # Obtenemos los datos de las variables de entorno que configuramos en el YAML
    host = os.getenv("POSTGRES_SERVER", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    user = "postgres"
    password = "password"
    db = "fastapi_db"
    
    # URL para asyncpg
    database_url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
    
    # Creamos el motor asíncrono
    engine = create_async_engine(database_url)
    
    try:
        async with engine.connect() as conn:
            # Esta es la prueba de fuego: ¿Podemos hablar con Postgres?
            result = await conn.execute(text("SELECT 1"))
            val = result.scalar()
            assert val == 1
    finally:
        await engine.dispose()

