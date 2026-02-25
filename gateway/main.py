from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import httpx
import jwt
import time
import logging
from typing import Any

# ACTIVITY 3: Request Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Gateway")

app = FastAPI(title="API Gateway", version="1.0.0")

# ACTIVITY 2: Add Authentication Config
SECRET_KEY = "my_super_secret_key"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="gateway/login")

# Service URLs (Activity 1 includes Course service on 8002)
SERVICES = {
    "student": "http://localhost:8001",
    "course": "http://localhost:8002"
}

# ACTIVITY 3: Add Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"Method: {request.method} Path: {request.url.path} Status: {response.status_code} Time: {formatted_process_time}ms")
    return response

# ACTIVITY 4: Error Handling (Global)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected Error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal gateway error occurred.", "error": str(exc)},
    )

# ACTIVITY 2: JWT Verification Logic
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ACTIVITY 4: Error Handling (Service Communication)
async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")
        
    url = f"{SERVICES[service]}{path}"
    
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")
                
            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code
            )
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail=f"The {service} service is offline. Please start it on port {SERVICES[service].split(':')[-1]}.")
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail=f"The {service} service took too long to respond.")
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Failed to communicate with {service} service: {str(e)}")

# ACTIVITY 2: Login Route for Token Generation
@app.post("/gateway/login")
def login():
    token = jwt.encode({"user": "admin"}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/")
def read_root():
    return {"message": "API Gateway is running", "available_services": list(SERVICES.keys())}

# --- STUDENT ROUTES ---

# Protected with JWT token
@app.get("/gateway/students")
async def get_all_students(token: dict = Depends(verify_token)):
    return await forward_request("student", "/api/students", "GET")

@app.get("/gateway/students/{student_id}")
async def get_student(student_id: int):
    return await forward_request("student", f"/api/students/{student_id}", "GET")

@app.post("/gateway/students")
async def create_student(body: dict):
    return await forward_request("student", "/api/students", "POST", json=body)

@app.put("/gateway/students/{student_id}")
async def update_student(student_id: int, body: dict):
    return await forward_request("student", f"/api/students/{student_id}", "PUT", json=body)

@app.delete("/gateway/students/{student_id}")
async def delete_student(student_id: int):
    return await forward_request("student", f"/api/students/{student_id}", "DELETE")

# --- COURSE ROUTES (ACTIVITY 1) ---

# Protected with JWT token
@app.get("/gateway/courses")
async def get_all_courses(token: dict = Depends(verify_token)):
    return await forward_request("course", "/api/courses", "GET")

@app.get("/gateway/courses/{course_id}")
async def get_course(course_id: int):
    return await forward_request("course", f"/api/courses/{course_id}", "GET")

@app.post("/gateway/courses")
async def create_course(body: dict):
    return await forward_request("course", "/api/courses", "POST", json=body)

@app.put("/gateway/courses/{course_id}")
async def update_course(course_id: int, body: dict):
    return await forward_request("course", f"/api/courses/{course_id}", "PUT", json=body)

@app.delete("/gateway/courses/{course_id}")
async def delete_course(course_id: int):
    return await forward_request("course", f"/api/courses/{course_id}", "DELETE")