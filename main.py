from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
  return {
    "message":"Backend AI Engineering Track Assignment",
    "status": "running"
  }

@app.get("/profile")
def profile():
  return {
    "name": "Juanito M. Ramos II",
    "track": "Backend AI Engineering",
    "specialization": {
      "Backend",
      "Cloud",
      "AI"
    }
  }