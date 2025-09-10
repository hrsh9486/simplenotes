from fastapi import FastAPI, HTTPException, Depends
from typing import List, Annotated
from uuid import UUID
from datetime import datetime, timedelta
import models, schemas
from db import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)



def getdb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(getdb)]

# Create todo
@app.post("/todos", response_model = schemas.TodoResponse)
async def create_todo(todo: schemas.TodoCreate, db: db_dependency):
    db_todo = models.TodoDB(description  = todo.description, dueDate=todo.dueDate)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Return all todos
@app.get("/todos", response_model = List[schemas.TodoResponse])
async def get_all_todos(db:db_dependency):
    result = db.query(models.TodoDB).all()
    return result

   
# Return specific todo
@app.get("/todos/{todo_id}", response_model = schemas.TodoResponse)
async def get_todo(todo_id:int, db:db_dependency):
    result = db.query(models.TodoDB).filter(models.TodoDB.id == todo_id).one_or_none()
    if not result:
        raise HTTPException(status_code=404, detail= 'Todo not found')
    if not result.isDeleted:
        return result
    else: return {"Todo Deleted"}


#Edit specific todo
@app.put("/todo/{todo_id}")
async def update_todo(todo_id: int, todo: schemas.TodoUpdate, db:db_dependency):
    result = db.query(models.TodoDB).filter(models.TodoDB.id == todo_id).one_or_none()
    if not result:
        raise HTTPException(status_code=404, detail= 'Todo not found')
    update_data = todo.model_dump(exclude_unset = True)
    for field, value in update_data.items():
        setattr(result, field, value)
    db.commit()
    return {"Todo Updated"}     


#Soft delete specific todo
@app.delete("/todos/{todo_id}")
async def soft_delete_todo(todo_id: int, db:db_dependency):
    result = db.query(models.TodoDB).filter(models.TodoDB.id == todo_id).one_or_none()
    if not result:
        raise HTTPException(status_code=404, detail= 'Todo not found')
    result.isDeleted = True
    db.commit()
    return {"Todo soft deleted"}

