import pytest
from httpx import AsyncClient,ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.core.database import Model, get_db

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

@pytest.fixture(autouse=True)
async def override_dependency(session):
    async def get_test_db():
        yield session

    app.dependency_overrides[get_db] = get_test_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac