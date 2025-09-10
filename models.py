from sqlalchemy import Column, Integer, String, Boolean, DateTime
from db import Base
import datetime


class TodoDB(Base):
    __tablename__ = 'Todos'

    id = Column(Integer, primary_key = True, index = True)
    description = Column(String, index = True)
    is_deleted = Column(Boolean, default= False)
    is_completed = Column(Boolean, default = False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    due_date = Column(DateTime, nullable=True)

