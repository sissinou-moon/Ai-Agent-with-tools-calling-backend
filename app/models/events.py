from app.database import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from sqlalchemy import String, Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime

class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, index=True)
    type: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), index=True)
    source: Mapped[str] = mapped_column(String)
    data: Mapped[dict] = mapped_column(JSONB)