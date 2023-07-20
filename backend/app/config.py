from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlalchemy.sql import select
from sqlalchemy import update
from datetime import datetime
from app.model import Props

DB_CONFIG = f"postgresql+asyncpg://postgres:postgres@localhost:5432/test"


class AsyncDatabaseSession:

    def __init__(self):
        self.session = None
        self.engine = None

    def __getattr__(self, name):
        return getattr(self.session, name)

    def init(self):
        self.engine = create_async_engine(DB_CONFIG, future=True, echo=True, pool_size=10, max_overflow=20)
        self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)()

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)


db = AsyncDatabaseSession()


async def upd_time_db():
    """ update DB change time"""
    query = select(Props).where(Props.prop == "upd_time")
    if (await db.execute(query)).scalar_one_or_none() is None:
        db.add(Props(
            prop="upd_time",
            val=str(datetime.now())
        ))
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    query = update(Props) \
        .where(Props.prop == "upd_time") \
        .values(**{'prop': 'upd_time', 'val': str(datetime.now())}) \
        .execution_options(synchronize_session="fetch")

    await db.execute(query)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise


async def commit_rollback():
    try:
        await db.commit()
        await upd_time_db()
    except Exception:
        await db.rollback()
        raise
