from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings
from app.core.db_utils import clean_database_url_for_asyncpg

settings = get_settings()

# Clean database URL and detect SSL requirement
db_url, ssl_required = clean_database_url_for_asyncpg(settings.database_url)

# Create engine with SSL support if required
if ssl_required:
    engine = create_async_engine(
        db_url,
        echo=False,
        future=True,
        connect_args={"ssl": "require"}
    )
else:
    engine = create_async_engine(db_url, echo=False, future=True)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
