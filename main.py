from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from uuid import UUID
from datetime import datetime, timedelta
import models
from db import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class TodoBase(BaseModel):
    id: UUID
    description: str
    is_deleted: bool = False
    dueDate: datetime
    createdAt: datetime

def getdb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(getdb)]

# Add todo
@app.post("/todos")
async def create_todo(todo: TodoBase, db: db_dependency):
    db_todo = models.TodoDB(description  = todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    db.commit()
    
# Return all todos
@app.get("/todos")
async def get_all_todos(db:db_dependency):
    result = db.query(models.TodoDB).all()
    if not result:
        raise HTTPException(status_code=404, detail= 'Todo not found')
    return result
    
# Return specific todo
@app.get("/todos/{todo_id}")
async def get_todo(todo_id:int, db:db_dependency):
    result = db.query(models.TodoDB).filter(models.TodoDB.id == todo_id).one_or_none()
    if not result:
        raise HTTPException(status_code=404, detail= 'Todo not found')
    if not result.is_deleted:
        return result
    else: return {"Todo Deleted"}


#Edit specific todo
@app.put("/todo/{todo_id}")
async def update_todo(todo_id: int, description: str, db:db_dependency):
    result = get_todo(todo_id, db)
    if not result:
        return None
    result.description = description
    db.commit()
    return {"Todo Updated"}     


#Soft delete specific todo
@app.delete("/todo/{todo_id}")
async def soft_delete_todo(todo_id: int, db:db_dependency):
    result = get_todo(todo_id, db)
    if not result:
        return None
    result.is_deleted = True
    db.commit()
    return {"Todo soft deleted"}

#Restore deleted todo
@app.put("/todo/{todo_id}")
async def restore_deleted_todo(todo_id: int, db:db_dependency):
    result = get_todo(todo_id, db)
    if not result:
        return None
    result.is_deleted = False
    db.commit()
    return {"Todo restored"}

#Hard delete specific todo
@app.delete("/todo/{todo_id}")
async def hard_delete_specific_todo(todo_id: int, db:db_dependency):
    result = get_todo(todo_id, db)
    if not result:
        return None
    db.delete(result)
    db.commit()
    return {"Todo Deleted"}

