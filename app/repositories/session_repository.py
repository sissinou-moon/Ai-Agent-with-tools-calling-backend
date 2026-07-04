from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession # THIS IS THE DATABASE CONNECTION , EVERY REQUEST GETS ITS OWN SESSION
from sqlalchemy import select
from uuid import UUID
from app.models.sessions import Session

class SessionRepository:


    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_new_session(self, **kwargs):
        session = Session(**kwargs)

        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)

        return session

    async def get_by_refresh_token(self, refresh_token: str) -> Session | None:
        result = await self.db.execute(
            select(Session).where(Session.refresh_token == refresh_token)
        )
        return result.scalar_one_or_none()

    async def revoke_session(self, session_id: UUID):
        await self.db.execute(
            update(Session)
            .where(Session.id == session_id)
            .values(is_active=False, revoked=True)
        )
        await self.db.commit()
        return True

    async def get_by_id(self, session_id: UUID) -> Session | None:
        result = await self.db.execute(
            select(Session).where(Session.id == session_id)
        )
        return result.scalar_one_or_none()

    async def revoke_all_sessions(self, user_id: UUID):
        await self.db.execute(
            update(Session)
            .where(Session.user_id == user_id)
            .values(is_active=False, revoked=True)
        )
    
        await self.db.commit()
        
        return True

        
