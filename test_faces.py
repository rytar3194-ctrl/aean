import os
import sys
import shutil

sys.path.append('backend')
from app.services.face_service import face_service

face_service.initialize()

images = [
    ("جبير الوتاري", r"C:\Users\user\.gemini\antigravity\brain\4aae1f03-6e2b-4b30-aa74-86e8d6981e15\.user_uploaded\media_1791772004723_22618f1d.jpg", "jubair_alwatari.jpg"),
    ("أمجد جاهوس", r"C:\Users\user\.gemini\antigravity\brain\4aae1f03-6e2b-4b30-aa74-86e8d6981e15\.user_uploaded\media_1791772108652_32b109d8.jpg", "amjad_jahwas.jpg"),
    ("حازم الرديني", r"C:\Users\user\.gemini\antigravity\brain\4aae1f03-6e2b-4b30-aa74-86e8d6981e15\.user_uploaded\media_1791772200066_1c811999.jpg", "hazem_alrudaini.jpg"),
]

os.makedirs("backend/uploads/students", exist_ok=True)
os.makedirs("frontend/public/students", exist_ok=True)
os.makedirs("frontend/src/assets/students", exist_ok=True)

for name, src, filename in images:
    # copy to uploads
    shutil.copyfile(src, os.path.join("backend/uploads/students", filename))
    shutil.copyfile(src, os.path.join("frontend/public/students", filename))
    shutil.copyfile(src, os.path.join("frontend/src/assets/students", filename))

    data = open(src, "rb").read()
    res = face_service.detect_and_extract(data)
    count = res.get("count", 0)
    dim = len(res["faces"][0]["embedding"]) if count > 0 else 0
    print(f"Student: {name} | File: {filename} | Faces detected: {count} | Vector Dim: {dim}")
