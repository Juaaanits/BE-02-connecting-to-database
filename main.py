from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from app.database import create_db_and_tables, seed_tasks, SessionDep
from sqlmodel import select
from app.models import Task


app = FastAPI()

class TaskCreate(BaseModel):
    title: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"error": "Invalid request"})


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_tasks()


@app.get("/")
def root():
    return {
        "message": "Backend AI Engineering Track Assignment",
        "status": "running"
    }


@app.get("/tasks")
def get_tasks(session: SessionDep):
    statement = select(Task)
    tasks = session.exec(statement).all()
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if task is None:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    return task


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, session: SessionDep):
    if task_data.title is None or task_data.title.strip() == "":
        return JSONResponse(status_code=400, content={"error": "Title is required"})

    new_task = Task(title=task_data.title, done=False)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: TaskUpdate, session: SessionDep):
    task = session.get(Task, task_id)
    if task is None:
        return JSONResponse(status_code=404, content={"error": "Task not found"})

    if task_data.title is None or task_data.title.strip() == "":
        return JSONResponse(status_code=400, content={"error": "Title is required"})
    if task_data.done is None:
        return JSONResponse(status_code=400, content={"error": "Done status is required"})

    task.title = task_data.title
    task.done = task_data.done

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if task is None:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    session.delete(task)
    session.commit()
