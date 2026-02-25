# gateway/main.py
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import httpx
import jwt
import time
import logging
from typing import Any

# ACTIVITY 3: Setup Basic Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Gateway")

app = FastAPI(title="API Gateway", version="1.0.0")

# Security Config
SECRET_KEY = "my_super_secret_key"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="gateway/login")

# Service URLs
SERVICES = {
    "student": "http://localhost:8001",
    "course": "http://localhost:8002"
}

# ACTIVITY 3: Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Process the request
    response = await call_next(request)
    
    # Calculate time and log details
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"Method: {request.method} Path: {request.url.path} Status: {response.status_code} Time: {formatted_process_time}ms")
    
    return response

# ACTIVITY 4: Global Error Handler for unexpected crashes
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected Error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal gateway error occurred.", "error": str(exc)},
    )

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")
        
    url = f"{SERVICES[service]}{path}"
    
    # ACTIVITY 4: Enhanced Error Handling for specific connection failures
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
            raise HTTPException(status_code=503, detail=f"The {service} service is offline. Please start it on its designated port.")
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail=f"The {service} service took too long to respond.")
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Failed to communicate with {service} service: {str(e)}")

@app.post("/gateway/login")
def login():
    token = jwt.encode({"user": "admin"}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/")
def read_root():
    return {"message": "API Gateway is running", "available_services": list(SERVICES.keys())}

@app.get("/gateway/students")
async def get_all_students(token: dict = Depends(verify_token)):
    return await forward_request("student", "/api/students", "GET")

@app.get("/gateway/students/{student_id}")
async def get_student(student_id: int):
    return await forward_request("student", f"/api/students/{student_id}", "GET")

# --- UPDATED POST ROUTE ---
@app.post("/gateway/students")
async def create_student(body: dict):
    return await forward_request("student", "/api/students", "POST", json=body)

# --- UPDATED PUT ROUTE ---
@app.put("/gateway/students/{student_id}")
async def update_student(student_id: int, body: dict):
    return await forward_request("student", f"/api/students/{student_id}", "PUT", json=body)

@app.delete("/gateway/students/{student_id}")
async def delete_student(student_id: int):
    return await forward_request("student", f"/api/students/{student_id}", "DELETE")

@app.get("/gateway/courses")
async def get_all_courses():
    return await forward_request("course", "/api/courses", "GET")