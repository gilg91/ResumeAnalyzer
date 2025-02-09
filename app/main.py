from fastapi import FastAPI
from app.api import resume  # Import the resume module

app = FastAPI()

# Include the resume API
app.include_router(resume.router, prefix="/resume", tags=["Resume Upload"])

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with file uploads!"}
