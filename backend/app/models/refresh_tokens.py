from app.db.db import Base
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Index
from datetime import datetime
from sqlalchemy.orm import relationship


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    token_hash = Column(String(255), nullable=False, unique=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked_at = Column(DateTime, nullable=True)

    replaced_by_token_id = Column(Integer, nullable=True)

    device_info = Column(String(255), nullable=True)

    user = relationship("User", back_populates="refresh_tokens")

