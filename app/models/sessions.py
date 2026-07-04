from uuid import UUID, uuid4

from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from datetime import datetime


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    refresh_token: Mapped[str] = mapped_column(String(255), nullable=False)

    user_agent: Mapped[str] = mapped_column(String(255), nullable=False)
    device_name: Mapped[str] = mapped_column(String(255))
    ip: Mapped[str] = mapped_column(String(45), nullable=False)  # IPv4 or IPv6

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)

    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)