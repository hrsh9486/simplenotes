from sqlalchemy import Column, Integer, String, Boolean, DateTime
from db import Base


class TodoDB(Base):
    __tablename__ = 'Todos'

    id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    description = Column(String, index = True)
    isDeleted = Column(Boolean, default= False)
    isCompleted = Column(Boolean, default = False)
    dueDate = Column(DateTime, nullable=True)

