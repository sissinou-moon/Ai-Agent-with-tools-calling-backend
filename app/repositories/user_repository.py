from sqlalchemy.ext.asyncio import AsyncSession # THIS IS THE DATABASE CONNECTION , EVERY REQUEST GETS ITS OWN SESSION
from sqlalchemy import select

from app.models.users import User


class UserRepository:

    def __init__(self, db:AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> User:
        user = User(**kwargs)

        self.db.add(user)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def is_verified(self, user_id: str, email: str) -> bool:
        if user_id:
            return await self.db.execute(
                select(User.is_verified).where(User.id == user_id)
            )

        else:
            return await self.db.execute(
                select(User.is_verified).where(User.email == email)
            )
        

    async def delete(self, user: User):
        await self.db.delete(user)
        await self.db.commit()