import time

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User


async def create_user(db_session: AsyncSession, tg_id: int, role: str | None = None):
    user = User(tg_id=tg_id, role=role)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


async def get_user_by_tg_id(db_session: AsyncSession, tg_id: int):
    result = await db_session.execute(select(User).where(User.tg_id == tg_id))
    return result.scalar_one_or_none()


async def get_all_users(db_session: AsyncSession):
    result = await db_session.execute(select(User))
    return result.scalars().all()


async def update_user(db_session: AsyncSession, tg_id: int, role: str = None, balance: int = None):
    user = await get_user_by_tg_id(db_session, tg_id)
    if user:
        updates = {
            "role": role,
            "balance": balance
        }
        for attr, value in updates.items():
            if value is not None:
                setattr(user, attr, value)
            
        await db_session.commit()
        await db_session.refresh(user)
    
    return user


async def delete_user(db_session: AsyncSession, tg_id: int):
    user = await get_user_by_tg_id(db_session, tg_id)
    if user:
        db_session.delete(user)
        await db_session.commit()
    return user
