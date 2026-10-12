# EYAN AI (عِيَان) — Master AI-Powered Attendance & Student Analytics System

> **Tagline:** See. Verify. Attend. (شاهد. تحقّق. احضر.)  
> **Brand Name:** EYAN AI — عِيَان  
> **Category:** AI Computer Vision Smart Attendance & Educational Analytics

---

## Technical Stack Architecture

- **Backend:** Python 3.11, FastAPI, SQLAlchemy 2.x, Pydantic v2, SQLite (PostgreSQL Ready), Uvicorn.
- **AI Face Engine:** InsightFace `buffalo_l` model (512-dimensional vector embeddings), OpenCV, ONNX Runtime.
- **Security & RBAC:** OAuth2 Bearer JWT Tokens, Passlib / Argon2id password hashing, Role-Based Access Control (`Admin`, `Instructor`).
- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Recharts, Lucide Icons, Axios.
- **Design System:** Deep Navy (`#111936`), Midnight (`#090D1F`), Indigo (`#423A9F`), Electric Violet (`#7047E8`), Soft Lavender (`#A996FF`), Light Background (`#F5F6FB`).
- **Localization:** Full Arabic (RTL) and English (LTR) language support with dynamic font stack (`Tajawal` / `Inter`).

---

## Rapid PowerShell Quickstart Guide

### 1. Backend Setup & Run

```powershell
# Navigate to backend directory
cd C:\Users\user\.gemini\antigravity\scratch\Smart-AI-Attendance\backend

# Create & activate Python virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install backend dependencies
pip install -r requirements.txt

# Run FastAPI backend dev server (Server will seed database automatically)
uvicorn app.main:app --reload --port 8000
```

*The API documentation is accessible at:* `http://localhost:8000/docs`

### 2. Frontend Setup & Run

```powershell
# Navigate to frontend directory
cd C:\Users\user\.gemini\antigravity\scratch\Smart-AI-Attendance\frontend

# Install node dependencies
npm install

# Run Vite dev server
npm run dev
```

*The EYAN AI Web Interface is accessible at:* `http://localhost:5173`

---

## Default Login Credentials

- **Administrator (Admin):**
  - Username: `admin`
  - Password: `admin123`
- **Course Instructor (Instructor):**
  - Username: `instructor`
  - Password: `instructor123`

---

## Automated PyTest Verification

```powershell
cd C:\Users\user\.gemini\antigravity\scratch\Smart-AI-Attendance\backend
.\venv\Scripts\pytest
```

---

## Database Models & Schema Summary

1. `User` & `Role`: RBAC user authentication with Argon2id hashing.
2. `Student`: Unique academic numbers, department, level, active status.
3. `Course`, `CourseSection`, `Enrollment`: Course offerings and section rosters.
4. `Session`: Lecture session state machine (`scheduled`, `open`, `closed`, `cancelled`).
5. `Attendance`: Transactional attendance logs with unique constraint `(session_id, student_id)` preventing duplicates.
6. `FaceEmbedding`: 512-D InsightFace vectors stored with model metadata.
7. `AuditLog`: Complete administrative audit trail for compliance and tracking.
8. `SystemSettings`: Dynamic system settings (face threshold, late grace period).
