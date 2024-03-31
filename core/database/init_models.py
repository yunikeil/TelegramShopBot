import logging

from sqlalchemy.ext.asyncio import create_async_engine

from core.database import Base
import core.settings.config as conf

logger = logging.getLogger("telegram")
engine = create_async_engine(conf.DATABASE_URL, echo=conf.ECHO_SQL)


async def init_models():
    if not conf.DEBUG and conf.DROP_TABLES:
        raise ValueError("This action is possible only when the debug is enabled!")

    async with engine.begin() as conn:
        if conf.DROP_TABLES:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Init models finished.")
