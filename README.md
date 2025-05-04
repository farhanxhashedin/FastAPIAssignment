🚗 Parking Management System A RESTful API backend built using FastAPI to manage parking slots, handle user bookings, and facilitate admin operations in a parking lot. The system uses JWT-based authentication, SQLAlchemy ORM, and supports role-based access for users and admins.

📁 Project Structure

Project Structure
parking_management/
├── app/
│ ├── init.py
│ ├── main.py
│ ├── config.py
│ ├── dependencies.py
│ ├── database.py
│ ├── models/
│ │ ├── init.py
│ │ ├── user.py
│ │ ├── parking_slot.py
│ │ ├── booking.py
│ │ └── feedback.py
│ ├── schemas/
│ │ ├── init.py
│ │ ├── user.py
│ │ ├── parking_slot.py
│ │ ├── booking.py
│ │ ├── feedback.py
│ │ └── token.py
│ ├── crud/
│ │ ├── init.py
│ │ ├── user.py
│ │ ├── parking_slot.py
│ │ ├── booking.py
│ │ └── feedback.py
│ ├── api/
│ │ ├── init.py
│ │ ├── endpoints/
│ │ │ ├── init.py
│ │ │ ├── auth.py
│ │ │ ├── users.py
│ │ │ ├── parking_slots.py
│ │ │ ├── bookings.py
│ │ │ ├── feedback.py
│ │ │ └── admin.py
│ │ └── api.py
│ └── core/
│ ├── init.py
│ ├── security.py
│ └── utils.py
└── tests/
├── init.py
├── conftest.py
├── test_auth.py
├── test_users.py
├── test_parking_slots.py
├── test_bookings.py
├── test_feedback.py
└── test_admin.py
🚀 Features 🔐 Authentication & User Management JWT-based secure authentication.

User registration and login.

Roles: user, admin.

Admins can manage all records; users can only manage their own bookings.

🅿️ Parking Slot Management View available slots (all authenticated users).

Add, update, and delete slots (admins only).

Slots have id, label, and status (free/occupied/maintenance).

📅 Booking Management Users can book available slots.

View personal booking history.

Cancel existing bookings.

🗣️ Feedback System Submit feedback related to bookings or slots.

View and manage feedback (admins only).

🛠️ Admin Tools Bulk operations: add/update slots.

Maintenance mode: disable specific/all slots temporarily.

🧪 Testing ✅ Tests written using pytest and TestClient.

🔍 Target: 70%+ code coverage.

Test files available in tests/ directory.

🛠️ Tech Stack Layer Technology Framework FastAPI Language Python 3.8+ Database SQLite + SQLAlchemy Auth JWT (FastAPI Security) Validation Pydantic Testing Pytest, TestClient Docs Swagger (auto-generated)

🔧 Setup Instructions

📥 Clone the repository git clone https://github.com/your-username/parking_management.git cd parking_management

📦 Create & activate a virtual environment python -m venv env source env/bin/activate # or env\Scripts\activate on Windows

📦 Install dependencies pip install -r requirements.txt

🗄️ Run database migrations No migrations system yet — ensure app/database.py creates tables on startup.

▶️ Run the server uvicorn app.main:app --reload Visit Swagger UI: http://127.0.0.1:8000/docs

🧪 Run Tests pytest --cov=app tests/

📮 API Documentation Auto-generated Swagger UI: http://localhost:8000/docs

ReDoc UI: http://localhost:8000/redoc

✅ Deliverables ✅ Complete source code with organized structure.

✅ Tests for key features.

✅ API documentation via Swagger.

✅ README with setup and usage instructions.
