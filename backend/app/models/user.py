# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Index
from datetime import datetime, timezone
from app.db.db import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index('idx_users_locked_until', 'locked_until'),  # For lockout queries
    )

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="user", nullable=False, index=True)  # For role-based queries
    disabled = Column(Boolean, default=False, index=True)  # For active user queries
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    locked_until = Column(DateTime, nullable=True, index=True)  # Account lockout timestamp
    failed_login_attempts = Column(Integer, default=0)  # Track consecutive failures
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken",back_populates="user", cascade="all, delete-orphan",)

    def __repr__(self):
        return f"<User(username={self.username}, role={self.role})>"

    def is_locked(self) -> bool:
        """Check if account is currently locked."""
        if self.locked_until is None:
            return False
        now = datetime.now(timezone.utc)
        locked_until = self.locked_until
        if locked_until.tzinfo is None:
            locked_until = locked_until.replace(tzinfo=timezone.utc)
        return locked_until > now
