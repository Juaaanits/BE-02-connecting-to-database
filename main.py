from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from app.database import create_db_and_tables, seed_tasks

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    done: bool

class TaskCreate(BaseModel):
    title: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: bool

tasks = [
    Task(id=1, title="Learn FastAPI", done=False),
    Task(id=2, title="Learn CRUD", done=False),
]

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_tasks()


@app.get("/")
def root():
    return {
        "message":"Backend AI Engineering Track Assignment",
        "status": "running"
    }

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = next((task for task in tasks if task.id == task_id), None)
    if task is None:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    return task

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate):
    if task_data.title is None or task_data.title.strip() == "":
        return JSONResponse(status_code=400, content={"error": "Title is required"})
    new_id = max((existing_task.id for existing_task in tasks), default=0) + 1
    new_task = Task(id=new_id, title=task_data.title, done=False)

    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: TaskUpdate):
    task = next((task for task in tasks if task.id == task_id), None)
    if task is None:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    if task_data.title is None or task_data.title.strip() == "":
        return JSONResponse(status_code=400, content={"error": "Title is required"})

    task.title = task_data.title
    task.done = task_data.done
    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    task = next((task for task in tasks if task.id == task_id), None)
    if task is None:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    tasks.remove(task)
