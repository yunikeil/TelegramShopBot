from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, asc

from app.models.product import Product


async def create_product(db_session: AsyncSession, catalog_id: int, value: str):
    product = Product(
        catalog_id=catalog_id,
        value=value,
    )
    db_session.add(product)
    await db_session.commit()
    await db_session.refresh(product)
    return product


async def get_product(db_session: AsyncSession, product_id: int):
    stmt = select(Product).where(Product.id == product_id)
    result = await db_session.execute(stmt)
    return result.scalar()


async def get_all_catalog_products(db_session: AsyncSession, catalog_id: int):
    stmt = select(Product).where(Product.catalog_id == catalog_id)
    result = await db_session.execute(stmt)
    return result.scalars().all()


async def update_product(db_session: AsyncSession, product_id: int, value: str):
    product = await get_product(db_session, product_id)
    if product:
        product.value = value
        await db_session.commit()
        await db_session.refresh(product)

    return product


async def delete_product(db_session: AsyncSession, product_id: int):
    product = await get_product(db_session, product_id)
    if product:
        await db_session.delete(product)
        await db_session.commit()
    
    return product
