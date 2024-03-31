from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.models.shopping_cart import ShoppingCart


async def create_shopping_cart(db_session: AsyncSession, catalog_id: int, user_id: int, count: int):
    shopping_cart = ShoppingCart(catalog_id=catalog_id, user_id=user_id, count=count)
    db_session.add(shopping_cart)
    await db_session.commit()
    await db_session.refresh(shopping_cart)
    return shopping_cart


async def get_shopping_cart_by_ids(db_session: AsyncSession, catalog_id: int, user_id: int):
    result = await db_session.execute(
        select(ShoppingCart)
        .where(ShoppingCart.catalog_id == catalog_id)
        .where(ShoppingCart.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def get_all_shopping_carts(db_session: AsyncSession, user_id: int, offset: int, limit: int):
    result = await db_session.execute(select(ShoppingCart).where(ShoppingCart.user_id == user_id).offset(offset).limit(limit))
    return result.scalars().all()


async def get_shopping_cart_count(db_session: AsyncSession, user_id: int):
    result = await db_session.execute(select(func.count(ShoppingCart.user_id)).where(ShoppingCart.user_id == user_id))
    return result.scalar()


async def update_shopping_cart(db_session: AsyncSession, catalog_id: int, user_id: int, count: int):
    shopping_cart = await get_shopping_cart_by_ids(db_session, catalog_id, user_id)
    if shopping_cart:
        shopping_cart.count = count
        await db_session.commit()
        await db_session.refresh(shopping_cart)
    return shopping_cart


async def delete_shopping_cart(db_session: AsyncSession, catalog_id: int, user_id: int):
    shopping_cart = await get_shopping_cart_by_ids(db_session, catalog_id, user_id)
    if shopping_cart:
        await db_session.delete(shopping_cart)
        await db_session.commit()
    return shopping_cart
