from app.db.db import Base
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Index
from datetime import datetime
from sqlalchemy.orm import relationship


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    __table_args__ = (
        Index('idx_refresh_tokens_user_expires', 'user_id', 'expires_at'),  # For cleanup queries
        Index('idx_refresh_tokens_revoked', 'revoked_at'),  # For active token queries
    )

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    token_hash = Column(String(255), nullable=False, unique=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False, index=True)  # For expiration checks
    revoked_at = Column(DateTime, nullable=True, index=True)  # For filtering active tokens

    replaced_by_token_id = Column(Integer, nullable=True)

    device_info = Column(String(255), nullable=True)

    user = relationship("User", back_populates="refresh_tokens")

