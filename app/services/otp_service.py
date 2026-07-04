from app.repositories.otp_repository import OTPRepository
from app.models.otps import OTP
import secrets
from datetime import datetime, timedelta, UTC
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

# pyrefly: ignore [missing-import]
import resend 
from app.core.config import settings

resend.api_key = settings.resend_api_key

class OTPService:

    OTP_LENGTH = 6
    OTP_EXPIRE_MINUTES = 5

    def __init__(self, db: AsyncSession):
        self.db = db
        self.otp_repository = OTPRepository(db)

    def generate(self) -> str:
        return f"{secrets.randbelow(1000000):06d}"

    def expires_at(self) -> datetime:
        return datetime.now(UTC) + timedelta(
            minutes=self.OTP_EXPIRE_MINUTES
        )

    def is_expired(self, expires_at: datetime) -> bool:
        return datetime.now(UTC) > expires_at

    async def save_otp(self, **kwargs):
        otp = OTP(**kwargs)

        self.db.add(otp)
        await self.db.commit()
        await self.db.refresh(otp)

        return otp
        
    async def sendEmailOTP(self, email: str, otp: str):
        await resend.Emails.send_async({
            "from": 'MCP <onboarding@resend.dev>',
            "to": email,
            "subject": "OTP Verification",
            "html": f"<p>Your OTP is: {otp}</p>",
        })