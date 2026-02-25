# Microservices Architecture with API Gateway - FastAPI

This project demonstrates a **Microservices Architecture** using **Python** and **FastAPI**.
It was developed for the **Modern Topics in IT (IT4020)** module.

---

## 🌍 GitHub Repository

The complete source code for this project is available on GitHub:

🔗 **Repository Link:**
[MTIT Lab 3 - Microservices Architecture](https://github.com/SandaruwanChandrasena/mtit_lab3_microservices.git)

Clone the repository using:

```bash
git clone https://github.com/SandaruwanChandrasena/mtit_lab3_microservices.git
cd mtit_lab3_microservices
```

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

# 🚀 How to Run the Project

## Step 1: Create Virtual Environment

Open terminal inside the root `microservices-fastapi` folder.

### Windows

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 2: Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## Step 3: Start All Services

### ✅ Option A — Using `run_all.bat` (Recommended for Windows)

Simply double-click the `run_all.bat` file in the root folder.

---

### ✅ Option B — Manual Start (Open 3 Terminals)

Make sure the virtual environment is activated in each terminal.

### Terminal 1 – Student Service

```powershell
cd student-service
uvicorn main:app --reload --port 8001
```

### Terminal 2 – Course Service

```powershell
cd course-service
uvicorn main:app --reload --port 8002
```

### Terminal 3 – API Gateway

```powershell
cd gateway
uvicorn main:app --reload --port 8000
```

---

# 🌐 Application URLs

| Service                  | URL                                                      |
| ------------------------ | -------------------------------------------------------- |
| API Gateway (Main Entry) | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Student Service          | [http://localhost:8001/docs](http://localhost:8001/docs) |
| Course Service           | [http://localhost:8002/docs](http://localhost:8002/docs) |

---

# 🔐 Testing the Gateway with JWT Authentication

## 1️⃣ Get Access Token

Send a **POST** request to:

```
http://localhost:8000/gateway/login
```

This is a mock authentication endpoint for lab purposes.

You will receive:

```json
{
  "access_token": "your_token_here"
}
```

---

## 2️⃣ Authorize in Swagger UI

### Step A – Open Swagger

Open:

```
http://localhost:8000/docs
```

### Step B – Click Authorize

Click the green **Authorize 🔒** button (top right corner).

### Step C – Enter Credentials

Enter the following:

```
Username: admin
Password: admin123
```

Then click **Authorize**.

After successful login, you will be able to access all protected endpoints through the Gateway.

---

## 📮 Using Postman

If testing with Postman:

1. Go to the **Authorization** tab
2. Select **Bearer Token**
3. Paste the `access_token` obtained from `/gateway/login`
4. Send your request

The request will now be authenticated and routed correctly through the API Gateway.

---

## 3️⃣ Call Protected Endpoints

After authorization, you can test:

```
GET     /gateway/students
GET     /gateway/courses
POST    /gateway/students
PUT     /gateway/students/{id}
DELETE  /gateway/students/{id}
```

All requests are routed through the API Gateway to their respective microservices.

---

# 📌 Bonus: run_all.bat File

Create a file named `run_all.bat` in the root folder and paste:

```bat
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

