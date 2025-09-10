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
    dueDate: datetime
    createdAt: datetime

def getdb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(getdb)]


@app.post("/todos")
async def create_todo(todo: TodoBase, db: db_dependency):
    db_todo = models.TodoDB(description  = todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    db.commit()
    
@app.get("/todos")
async def get_all_todos(db:db_dependency):
    result = db.query(models.TodoDB).all()
    if not result:
        raise HTTPException(status_code=404, detail= 'Todo not found')
    return result
    


@app.get("/todos/{todo_id}")
async def get_todo(todo_id:int, db:db_dependency):
    result = db.query(models.TodoDB).filter(models.TodoDB.id == todo_id).first
    if not result:
        raise HTTPException(status_code=404, detail= 'Todo not found')
    return result

@app.delete("/todo/{todo_id}")
async def delete_specific_todo(todo_id: int, db:db_dependency):
    db.delete(models.TodoDB.id == todo_id)
    return {"Todo Deleted"}
