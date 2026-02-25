# Microservices Architecture with API Gateway - FastAPI

This project demonstrates a **Microservices Architecture** using **Python** and **FastAPI**.
It was developed for the **Modern Topics in IT (IT4020)** module.

🔗 **Repository Link:**  
[MTIT Lab 3 - Microservices Architecture](https://github.com/SandaruwanChandrasena/mtit_lab3_microservices.git)

---

## 📁 Project Structure

```
microservices-fastapi/
├── requirements.txt          # All Python dependencies
├── run_all.bat               # Windows script to start all services simultaneously
│
├── student-service/          # Microservice 1 (Port 8001)
│   ├── models.py             # Data models (Student schema)
│   ├── data_service.py       # Mock database operations
│   ├── service.py            # Business logic layer
│   └── main.py               # FastAPI app with API endpoints
│
├── course-service/           # Microservice 2 (Port 8002)
│   ├── models.py             # Data models (Course schema)
│   └── main.py               # FastAPI app with mock DB and endpoints
│
└── gateway/                  # API Gateway (Port 8000)
    └── main.py               # Gateway app with routing, JWT auth, logging, and error handling
```

---

## 🚀 How to Run the Project

### Step 1: Create Virtual Environment

Open terminal inside the root `microservices-fastapi` folder:

### Windows:

```
python -m venv venv
.\venv\Scripts\activate
```

### Mac/Linux:

```
python3 -m venv venv
source venv/bin/activate
```

---

### Step 2: Install Dependencies

```
pip install -r requirements.txt
```

---

### Step 3: Start All Services

#### ✅ Option A — Using `run_all.bat` (Recommended for Windows)

Double-click `run_all.bat` inside the root folder.

---

#### ✅ Option B — Manual Start (Open 3 Terminals)

Make sure virtual environment is activated in each terminal.

### Terminal 1

```
cd student-service
uvicorn main:app --reload --port 8001
```

### Terminal 2

```
cd course-service
uvicorn main:app --reload --port 8002
```

### Terminal 3

```
cd gateway
uvicorn main:app --reload --port 8000
```

---

## 🌐 Application URLs

| Service                  | URL                                                      |
| ------------------------ | -------------------------------------------------------- |
| API Gateway (Main Entry) | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Student Service          | [http://localhost:8001/docs](http://localhost:8001/docs) |
| Course Service           | [http://localhost:8002/docs](http://localhost:8002/docs) |

---

## 🔐 Testing the Gateway with JWT Authentication

### 1️⃣ Get Access Token

Send a **POST** request to:

```
http://localhost:8000/gateway/login
```

⚠ This is a mock authentication endpoint for lab purposes.
No request body is required.

You will receive:

```
{
  "access_token": "your_token_here"
}
```

---

### 2️⃣ Authorize in Swagger UI

1. Open: [http://localhost:8000/docs](http://localhost:8000/docs)
2. Click the green **Authorize 🔒** button
3. Paste your token
4. Click **Authorize**

If using Postman:

* Go to **Authorization**
* Select **Bearer Token**
* Paste the token

---

### 3️⃣ Call Protected Endpoints

Now you can test:

```
GET     /gateway/students
GET     /gateway/courses
POST    /gateway/students
PUT     /gateway/students/{id}
DELETE  /gateway/students/{id}
```

All requests will route through the API Gateway to their respective microservices.

---

# 📌 Bonus: `run_all.bat` File

Create a file named `run_all.bat` inside the root folder and paste:

```
@echo off
echo Starting Microservices Architecture...

echo Starting Student Service (Port 8001)...
start cmd /k ".\venv\Scripts\activate && cd student-service && uvicorn main:app --reload --port 8001"

echo Starting Course Service (Port 8002)...
start cmd /k ".\venv\Scripts\activate && cd course-service && uvicorn main:app --reload --port 8002"

echo Starting API Gateway (Port 8000)...
start cmd /k ".\venv\Scripts\activate && cd gateway && uvicorn main:app --reload --port 8000"

echo All services are booting up in separate windows!
```
