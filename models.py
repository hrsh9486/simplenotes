from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from db import Base
import uuid


class TodoDB(Base):
    __tablename__ = 'Todos'

    id = Column(UUID(as_uuid = True), primary_key = True, index = True, default = uuid.uuid4)
    description = Column(String, index = True)
    isDeleted = Column(Boolean, default= False)
    isCompleted = Column(Boolean, default = False)
    dueDate = Column(DateTime, nullable=True)

