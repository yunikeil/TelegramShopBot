from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, asc

from app.models.catalog import Catalog


async def create_catalog(
    db_session: AsyncSession,
    name: str,
    description: str,
    price: int,
    count: int,
    file_id: str | None = None,
):
    catalog = Catalog(name=name, description=description, price=price, count=count)
    db_session.add(catalog)
    await db_session.commit()
    await db_session.refresh(catalog)
    return catalog


async def get_catalog_by_id(db_session: AsyncSession, catalog_id: int):
    result = await db_session.execute(select(Catalog).where(Catalog.id == catalog_id))
    return result.scalar_one_or_none()


async def get_all_catalogs(db_session: AsyncSession, offset: int = 0, limit: int = 10):
    result = await db_session.execute(
        select(Catalog).order_by(Catalog.id).offset(offset).limit(limit)
    )
    return result.scalars().all()


async def get_catalogs_count(db_session: AsyncSession):
    result = await db_session.execute(select(func.count(Catalog.id)))
    return result.scalar()


async def update_catalog(
    db_session: AsyncSession,
    catalog_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    price: Optional[int] = None,
    count: Optional[int] = None,
    file_id: Optional[int] = None,
) -> Optional[Catalog]:
    catalog = await get_catalog_by_id(db_session, catalog_id)
    if catalog:
        updates = {
            "name": name,
            "description": description,
            "price": price,
            "count": count,
            "file_unique_tg_id": file_id,
        }

        for attr, value in updates.items():
            if value is not None:
                setattr(catalog, attr, value)

        await db_session.commit()
        await db_session.refresh(catalog)

    return catalog


async def delete_catalog(db_session: AsyncSession, catalog_id: int):
    catalog = await get_catalog_by_id(db_session, catalog_id)
    if catalog:
        await db_session.delete(catalog)
        await db_session.commit()
    return catalog
