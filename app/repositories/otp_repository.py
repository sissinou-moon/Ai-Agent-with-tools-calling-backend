from app.models.otps import OTP
from app.database import Base
# pyrefly: ignore [missing-import]
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from datetime import datetime, UTC

class OTPRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, user_id: UUID) -> OTP:
        result = await self.db.execute(
            select(OTP).where(OTP.user_id == user_id).where(OTP.purpose == "registration").where(OTP.is_verified == False).where(OTP.expires_at > datetime.now(UTC)).order_by(OTP.expires_at.desc()).limit(1)
        )
        return result.scalar_one_or_none()