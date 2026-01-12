from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.db.db import Base
from sqlalchemy.orm import relationship


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="tasks")
