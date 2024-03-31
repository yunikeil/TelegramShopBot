from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from app.models.catalog import Catalog


async def create_catalog(db_session: AsyncSession, name: str, description: str, count: int):
    catalog = Catalog(name=name, description=description, count=count)
    db_session.add(catalog)
    await db_session.commit()
    await db_session.refresh(catalog)
    return catalog


async def get_catalog_by_id(db_session: AsyncSession, catalog_id: int):
    result = await db_session.execute(select(Catalog).where(Catalog.id == catalog_id))
    return result.scalar_one_or_none()


async def get_all_catalogs(db_session: AsyncSession, offset: int = 0, limit: int = 10):
    result = await db_session.execute(select(Catalog).offset(offset).limit(limit))
    return result.scalars().all()


async def get_catalogs_count(db_session: AsyncSession):
    result = await db_session.execute(select(func.count(Catalog.id)))
    return result.scalar()


async def update_catalog(db_session: AsyncSession, catalog_id: int, name: str, description: str, count: int):
    catalog = await get_catalog_by_id(db_session, catalog_id)
    if catalog:
        catalog.name = name
        catalog.description = description
        catalog.count = count
        await db_session.commit()
        await db_session.refresh(catalog)
    return catalog


async def delete_catalog(db_session: AsyncSession, catalog_id: int):
    catalog = await get_catalog_by_id(db_session, catalog_id)
    if catalog:
        db_session.delete(catalog)
        await db_session.commit()
    return catalog
