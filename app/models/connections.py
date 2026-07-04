from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from sqlalchemy import String, Boolean, DateTime, Integer
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime


class Connection(Base):
    __tablename__ = "connections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, index=True)
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), index=True)
    access_token: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    data: Mapped[dict] = mapped_column(JSONB)
    app: Mapped[str] = mapped_column(String)