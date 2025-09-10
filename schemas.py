from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

# --- Request models ---

class TodoCreate(BaseModel):
    description: str
    dueDate: datetime

class TodoUpdate(BaseModel):
    description: str | None = None
    isCompleted: bool | None = None
    dueDate: datetime | None = None

# --- Response models ---

class TodoResponse(BaseModel):
    id: UUID 
    description: str
    isDeleted: bool
    isCompleted: bool
    dueDate: datetime

    class Config:
        orm_mode = True  # tells Pydantic it can read SQLAlchemy objects
