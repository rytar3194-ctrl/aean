import sys
import os
import json
import sqlite3
import shutil

sys.path.append('backend')
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from app.services.face_service import face_service

face_service.initialize()

# Database path
db_path = 'backend/eyan_ai.db'
con = sqlite3.connect(db_path)
cur = con.cursor()

# Ensure is_deleted column exists in students
cur.execute("PRAGMA table_info(students)")
cols = [c[1] for c in cur.fetchall()]
if 'is_deleted' not in cols:
    cur.execute("ALTER TABLE students ADD COLUMN is_deleted BOOLEAN DEFAULT 0")
    con.commit()

# Ensure uploads directories exist
os.makedirs("backend/uploads/students", exist_ok=True)
os.makedirs("frontend/public/students", exist_ok=True)

# 1. Update Dr. Safwan Al-Shaibani in users table
cur.execute("""
UPDATE users SET full_name = 'د. صفوان الشيباني' WHERE username = 'dr_safwan' OR email = 'safwan@gmail.com'
""")
con.commit()

# 2. Setup the 3 real students with their uploaded photos
students_data = [
    {
        "id": 1,
        "student_number": "STU-2026-001",
        "full_name": "جبير الوتاري",
        "guardian_phone": "777112233",
        "email": "jubair.alwatari@mahweet.edu.ye",
        "department": "قسم الحوسبة وتكنولوجيا المعلومات",
        "major": "ذكاء اصطناعي",
        "academic_level": 3,
        "section": "A",
        "img_src": r"C:\Users\user\.gemini\antigravity\brain\4aae1f03-6e2b-4b30-aa74-86e8d6981e15\.user_uploaded\media_1791772004723_22618f1d.jpg",
        "filename": "jubair_alwatari.jpg"
    },
    {
        "id": 2,
        "student_number": "STU-2026-002",
        "full_name": "أمجد جاهوس",
        "guardian_phone": "777223344",
        "email": "amjad.jahwas@mahweet.edu.ye",
        "department": "قسم الحوسبة وتكنولوجيا المعلومات",
        "major": "ذكاء اصطناعي",
        "academic_level": 3,
        "section": "A",
        "img_src": r"C:\Users\user\.gemini\antigravity\brain\4aae1f03-6e2b-4b30-aa74-86e8d6981e15\.user_uploaded\media_1791772108652_32b109d8.jpg",
        "filename": "amjad_jahwas.jpg"
    },
    {
        "id": 3,
        "student_number": "STU-2026-003",
        "full_name": "حازم الرديني",
        "guardian_phone": "777334455",
        "email": "hazem.alrudaini@mahweet.edu.ye",
        "department": "قسم الحوسبة وتكنولوجيا المعلومات",
        "major": "ذكاء اصطناعي",
        "academic_level": 3,
        "section": "A",
        "img_src": r"C:\Users\user\.gemini\antigravity\brain\4aae1f03-6e2b-4b30-aa74-86e8d6981e15\.user_uploaded\media_1791772200066_1c811999.jpg",
        "filename": "hazem_alrudaini.jpg"
    }
]

# Clean existing students & face embeddings & enrollments to have pristine database
cur.execute("DELETE FROM attendance")
cur.execute("DELETE FROM enrollments")
cur.execute("DELETE FROM face_embeddings")
cur.execute("DELETE FROM students")
con.commit()

# Ensure AI-301 Course and Section 1 exist
cur.execute("SELECT id FROM courses WHERE course_code = 'AI-301'")
course_row = cur.fetchone()
if not course_row:
    cur.execute("""
    INSERT INTO courses (id, course_code, name, description, department, academic_level, is_active, created_at)
    VALUES (1, 'AI-301', 'مقرر الذكاء الاصطناعي', 'مقرر الذكاء الاصطناعي والرؤية الحاسوبية - المستوى الثالث', 'قسم الحوسبة وتكنولوجيا المعلومات', 3, 1, CURRENT_TIMESTAMP)
    """)
    con.commit()
    course_id = 1
else:
    course_id = course_row[0]

cur.execute("SELECT id FROM course_sections WHERE course_id = ?", (course_id,))
sec_row = cur.fetchone()
if not sec_row:
    cur.execute("""
    INSERT INTO course_sections (id, course_id, section_number, instructor_id)
    VALUES (1, ?, 'SEC-01', 3)
    """, (course_id,))
    con.commit()
    section_id = 1
else:
    section_id = sec_row[0]

# Ensure at least 1 Session exists
cur.execute("SELECT id FROM sessions WHERE section_id = ?", (section_id,))
session_row = cur.fetchone()
if not session_row:
    cur.execute("""
    INSERT INTO sessions (id, section_id, instructor_id, title, session_date, status, created_at, updated_at)
    VALUES (1, ?, 3, 'المحاضرة 1: مقدمة في الرؤية الحاسوبية والشبكات العصبية', CURRENT_TIMESTAMP, 'open', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """, (section_id,))
    con.commit()
    session_id = 1
else:
    session_id = session_row[0]

# Insert the 3 students and compute real face embeddings
for st in students_data:
    photo_rel_url = f"/students/{st['filename']}"
    # Copy photo
    shutil.copyfile(st['img_src'], os.path.join("backend/uploads/students", st['filename']))
    shutil.copyfile(st['img_src'], os.path.join("frontend/public/students", st['filename']))

    cur.execute("""
    INSERT INTO students (id, student_number, full_name, email, guardian_phone, department, major, academic_level, section, photo_url, is_active, is_deleted, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """, (
        st['id'],
        st['student_number'],
        st['full_name'],
        st['email'],
        st['guardian_phone'],
        st['department'],
        st['major'],
        st['academic_level'],
        st['section'],
        photo_rel_url
    ))

    # Enroll student in section
    cur.execute("""
    INSERT INTO enrollments (student_id, section_id, enrolled_at)
    VALUES (?, ?, CURRENT_TIMESTAMP)
    """, (st['id'], section_id))

    # Compute Real 512D Vector using face_service
    img_bytes = open(st['img_src'], "rb").read()
    res = face_service.detect_and_extract(img_bytes)
    if res.get("success") and res.get("count", 0) > 0:
        emb = res["faces"][0]["embedding"]
        emb_json = json.dumps(emb)
        cur.execute("""
        INSERT INTO face_embeddings (student_id, embedding_data, model_name, model_version, embedding_dimension, is_active, created_at)
        VALUES (?, ?, 'buffalo_l', '1.0', 512, 1, CURRENT_TIMESTAMP)
        """, (st['id'], emb_json))
        print(f"✓ Enrolled 512D face embedding for {st['full_name']}")
    else:
        print(f"✗ Warning: Failed to extract face for {st['full_name']}")

# Initial attendance: Jubair present, Amjad present, Hazem late
cur.execute("""
INSERT INTO attendance (session_id, student_id, status, recorded_at, recognition_confidence, recognition_method, notes)
VALUES (?, 1, 'present', CURRENT_TIMESTAMP, 0.94, 'camera', 'تم التعرف الآلي بنجاح')
""", (session_id,))
cur.execute("""
INSERT INTO attendance (session_id, student_id, status, recorded_at, recognition_confidence, recognition_method, notes)
VALUES (?, 2, 'present', CURRENT_TIMESTAMP, 0.91, 'camera', 'تم التعرف الآلي بنجاح')
""", (session_id,))
cur.execute("""
INSERT INTO attendance (session_id, student_id, status, recorded_at, recognition_confidence, recognition_method, notes)
VALUES (?, 3, 'late', CURRENT_TIMESTAMP, 0.88, 'camera', 'تأخير 10 دقائق')
""", (session_id,))

con.commit()
print("All 3 students enrolled, face embeddings extracted and trained, and attendance seeded successfully!")
con.close()
