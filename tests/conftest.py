import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from fastapi.testclient import TestClient


from app.main import app
from app.core.database import Model

TEST_DATABASE_URL = 'sqlite+aiosqlite:///:memory:'


@pytest.fixture
async def session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

    async_session = async_sessionmaker(engine,class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session


    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
def client():
    return TestClient(app)