from fastapi import FastAPI,status, HTTPException
from database import Base, engine, ToDo
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Create ToDoRequest Base Model
class ToDoRequest(BaseModel):
    task: str


Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
def root():
    return "welcome to my app"

@app.post("/todo", status_code = status.HTTP_201_CREATED)
def create_todo(todo: ToDoRequest):
    session = Session(bind=engine, expire_on_commit=False)
    tododb = ToDo(task = todo.task)
    session.add(tododb)
    session.commit()
    id = tododb.id
    session.close()
    return f"created todo item with id {id}"

@app.get("/todo/{id}")
def read_todo(id: int):
    session =  Session(bind=engine, expire_on_commit=False)
    todo = session.query(ToDo).get(id)
    session.close()
    return f"todo item with id: {todo.id} and task: {todo.task}"

@app.put("/todo/{id}")
def update_todo(id: int, task: str):
    session = Session(bind=engine, expire_on_commit=False)
    todo = session.query(ToDo).get(id)
    if todo:
        todo.task = task
        session.commit()
    session.close()
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")
    return "update todo item with id {id}"

@app.delete("/todo/{id}")
def delete_todo(id: int):
    session = Session(bind=engine, expire_on_commit=False)
    todo = session.query(ToDo).get(id)
    if todo:
        session.delete(todo)
        session.commit()
        session.close()
    else:
        raise HTTPException(status=404, details = "deleted")
    return None

@app.get("/todo")
def read_todo_list():
    session = Session(bind=engine, expire_on_commit=False)
    todo = session.query(ToDo).all()
    return todo
