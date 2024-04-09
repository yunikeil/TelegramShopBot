from typing import Optional
from random import choice

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, asc

from app.models.purchase import Purchase
from app.services.catalog import get_catalog_by_id
from app.services.product import get_all_catalog_products


async def create_purchase(
    db_session: AsyncSession, user_id: int, catalog_id: int,
):
    catalog = await get_catalog_by_id(db_session, catalog_id)
    if not catalog:
        return None

    products = await get_all_catalog_products(db_session, catalog_id)
    if not products:
        return None
    product = choice(products)
    
    purchase = Purchase(
        tg_id=user_id,
        name=catalog.name,
        description=catalog.description,
        price=catalog.price,
        file_unique_tg_id=catalog.file_unique_tg_id,
        value=product.value,
    )

    await db_session.delete(product)
    await db_session.add(purchase)
    await db_session.commit()
    await db_session.refresh(purchase)
    
    return purchase


async def get_purchase(db_session: AsyncSession, purchase_id: int):
    stmt = select(Purchase).where(Purchase.id == purchase_id)
    result = await db_session.execute(stmt)
    return result.scalar_one_or_none()


async def get_all_purchase(db_session: AsyncSession, user_id: int):
    stmt = select(Purchase).where(Purchase.tg_id == user_id)
    result = await db_session.execute(stmt)
    return result.scalars().all()


async def get_purchase_count(db_session: AsyncSession, user_id: int):
    stmt = select(func.count(Purchase.id)).where(Purchase.tg_id == user_id)
    result = await db_session.execute(stmt)
    return result.scalar()


async def update_purchase(db_session: AsyncSession, purchase_id: int):
    pass


async def delete_purchase(db_session: AsyncSession, user_id: int, purchase_id: int):
    pass
