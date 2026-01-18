"""
Login Attempts Model

Tracks failed login attempts for account lockout mechanism.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db.db import Base
from datetime import datetime, timezone


class LoginAttempt(Base):
    __tablename__ = "login_attempts"
    __table_args__ = (
        Index('idx_login_attempts_username_time', 'username', 'attempted_at'),  # For user login history
    )

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)
    ip_address = Column(String, nullable=True, index=True)  # For IP-based analysis
    success = Column(Integer, default=0, index=True)  # 0 = failed, 1 = success
    attempted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)  # For time-based queries

    def __repr__(self):
        return f"<LoginAttempt(username={self.username}, success={self.success}, attempted_at={self.attempted_at})>"
