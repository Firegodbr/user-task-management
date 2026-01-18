from sqlalchemy import Column, Integer, String, Date, ForeignKey, Index
from app.db.db import Base
from sqlalchemy.orm import relationship


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        Index('idx_tasks_user_date', 'user_id', 'date'),  # Composite index for pagination queries
    )

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, nullable=False)
    date = Column(Date, nullable=False, index=True)  # Index for date sorting
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # Index for user filtering
    user = relationship("User", back_populates="tasks")
