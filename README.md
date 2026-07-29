# BE-02 Connecting CRUD to SQLite Database

## Overview

This project is my Week 3 assignment for the FlyRank Backend AI Engineering track.

The objective is to replace the in-memory task storage from the previous assignment with a persistent SQLite database while keeping the API contract unchanged. The application automatically creates the database and required tables on startup, allowing task data to persist across server restarts.

This assignment demonstrates one of the core principles of backend engineering:

> **The API defines what the application does, while the database defines where the data is stored.**

---

## Assignment Objectives

- Replace the in-memory task list with SQLite.
- Implement persistent CRUD operations.
- Automatically create the database and tables.
- Seed sample tasks only during the first application startup.
- Maintain the exact same REST API from Assignment 1.
- Practice basic SQL operations using SQLite.

---

## Tech Stack

- Python 3
- FastAPI
- SQLite
- SQLModel _(or sqlite3 depending on implementation)_
- Uvicorn
- DB Browser for SQLite _(used for database inspection)_

---

## Project Structure

```text
BE-02-connecting-to-database/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routes.py
│
├── tasks.db
├── requirements.txt
├── README.md
├── .gitignore
└── assets/
    ├── swagger.png
    ├── database.png
    └── sql-query.png
```

---

## Database Schema

The application automatically creates a SQLite database named:

```text
tasks.db
```

The database contains a single table:

| Column | Type    | Description            |
| ------ | ------- | ---------------------- |
| id     | Integer | Primary Key            |
| title  | Text    | Task title             |
| done   | Boolean | Task completion status |

During the first application startup, three sample tasks are automatically inserted if the table is empty.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Juaaanits/BE-02-connecting-to-database.git
```

Move into the project directory:

```bash
cd BE-02-connecting-to-database
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

**Windows**

```bash
.venv\Scripts\activate
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the FastAPI development server:

```bash
fastapi dev
```

The API will be available at:

```
http://127.0.0.1:8000
```

The first time the application starts:

- `tasks.db` is created automatically.
- The `tasks` table is created automatically.
- Three sample tasks are inserted only if the table is empty.

---

# API Endpoints

## GET /tasks

Returns all tasks.

Example response:

```json
[
  {
    "id": 1,
    "title": "Learn FastAPI",
    "done": false
  }
]
```

---

## GET /tasks/{id}

Returns a single task.

Unknown IDs return:

```json
{
  "error": "Task not found"
}
```

---

## POST /tasks

Creates a new task.

Example request:

```json
{
  "title": "Study SQLite"
}
```

Example response:

```json
{
  "id": 4,
  "title": "Study SQLite",
  "done": false
}
```

---

## PUT /tasks/{id}

Updates an existing task.

Example request:

```json
{
  "title": "Learn SQL",
  "done": true
}
```

---

## DELETE /tasks/{id}

Deletes a task.

---

## Interactive API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# Database Viewer

The project was tested using **DB Browser for SQLite**.

Example database view:

```sql
SELECT * FROM tasks;
```

<img src="assets/database.png" width="900">

---

## Example SQL Queries

Retrieve all tasks

```sql
SELECT * FROM tasks;
```

Retrieve completed tasks

```sql
SELECT * FROM tasks
WHERE done = 1;
```

Count all tasks

```sql
SELECT COUNT(*)
FROM tasks;
```

Mark all tasks as completed

```sql
UPDATE tasks
SET done = 1;
```

Delete completed tasks

```sql
DELETE FROM tasks
WHERE done = 1;
```

---

## Example cURL Requests

Retrieve all tasks

```bash
curl http://127.0.0.1:8000/tasks
```

Create a task

```bash
curl -X POST http://127.0.0.1:8000/tasks \
-H "Content-Type: application/json" \
-d "{\"title\":\"Study SQL\"}"
```

Delete a task

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

---

## Learning Outcomes

Through this assignment I learned how to:

- Connect a FastAPI application to SQLite.
- Create and initialize a relational database automatically.
- Perform CRUD operations using SQL.
- Persist application data across server restarts.
- Separate the API layer from the data storage layer.
- Understand how backend applications interact with relational databases.

---

## Key Backend Concept

The client never knows how data is stored.

Assignment 1

```text
Client
   │
FastAPI
   │
In-memory Array
```

Assignment 2

```text
Client
   │
FastAPI
   │
SQLite Database
```

The API endpoints remain exactly the same—the storage implementation changes.

---

## Future Improvements

- Search tasks using SQL `LIKE`
- Filter completed tasks
- Sort tasks alphabetically
- Add task statistics endpoint
- Store timestamps (`created_at`, `updated_at`)
- Migrate to PostgreSQL
- Introduce SQLAlchemy and Alembic migrations

---

## License

This project was created for educational purposes as part of the FlyRank Backend AI Engineering program.
