from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine, select

from app.models import Task

sqlite_file_name = "tasks.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

def seed_tasks():
    with Session(engine) as session:
        # Check if tasks already exist in the database
        existing_tasks = session.exec(select(Task).limit(1)).all()
        if not existing_tasks:
            # If no tasks exist, seed the database with initial tasks
            initial_tasks = [
                Task(title="Learn FastAPI", done=False),
                Task(title="Learn CRUD", done=False),
                Task(title="Finish Week3", done=False),
            ]
            session.add_all(initial_tasks)
            session.commit()

SessionDep = Annotated[Session, Depends(get_session)]
