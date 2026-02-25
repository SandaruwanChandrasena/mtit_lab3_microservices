from fastapi import FastAPI
from models import Course

app = FastAPI(title="Course Service")

# Mock database
courses = [{"id": 1, "name": "Modern Topics in IT", "credits": 4}]

@app.get("/api/courses")
def get_courses():
    return courses