# pyrefly: ignore [missing-import]

from app.models.audit import Audit
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

class AuditService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_event(
        self,
        **kwargs,
    ):
        audit = Audit(**kwargs)
        self.db.add(audit)
        await self.db.commit()
        await self.db.refresh(audit)

        return audit
