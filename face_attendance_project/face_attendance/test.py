"""
test.py  —  LOCAL MACHINE PE CHALAO (webcam chahiye)
Ye script cloud pe kaam nahi karti.
Controls:
  O  →  Attendance save karein
  Q  →  Quit
"""

import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier

# ── Windows Voice (optional) ──────────────────────────────────────────────────
def speak(text):
    try:
        from win32com.client import Dispatch
        engine = Dispatch("SAPI.SpVoice")
        engine.Speak(text)
    except Exception:
        print(f"[Voice] {text}")   # Linux/Mac fallback

# ── Paths ─────────────────────────────────────────────────────────────────────
DATA_DIR       = "data"
ATTENDANCE_DIR = "Attendance"
CASCADE_PATH   = os.path.join(DATA_DIR, "haarcascade_frontalface_default.xml")
NAMES_PATH     = os.path.join(DATA_DIR, "names.pkl")
FACES_PATH     = os.path.join(DATA_DIR, "faces_data.pkl")
BG_PATH        = "background.png"

os.makedirs(ATTENDANCE_DIR, exist_ok=True)

# ── Validate files ────────────────────────────────────────────────────────────
for path in [CASCADE_PATH, NAMES_PATH, FACES_PATH]:
    if not os.path.exists(path):
        print(f"❌ File nahi mili: {path}")
        print("   Pehle add_faces.py chalao.")
        exit()

# ── Load model ────────────────────────────────────────────────────────────────
with open(NAMES_PATH, "rb") as f:
    LABELS = pickle.load(f)
with open(FACES_PATH, "rb") as f:
    FACES  = pickle.load(f)

print(f"✅ Data loaded — Faces shape: {FACES.shape} | Labels: {len(LABELS)}")

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

# ── Camera & cascade ──────────────────────────────────────────────────────────
video      = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier(CASCADE_PATH)

# Background (optional)
imgBackground = cv2.imread(BG_PATH) if os.path.exists(BG_PATH) else None

COL_NAMES = ["NAME", "TIME"]
print("🎥 Camera shuru ho gaya!")
print("   O dabao → attendance lein | Q dabao → band karein")

while True:
    ret, frame = video.read()
    if not ret:
        print("❌ Frame nahi mila.")
        break

    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    attendance_entry = None

    for (x, y, w, h) in faces:
        crop      = frame[y:y+h, x:x+w]
        resized   = cv2.resize(crop, (50, 50)).flatten().reshape(1, -1)
        output    = knn.predict(resized)
        name      = str(output[0])

        ts        = time.time()
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")

        # Draw box + label
        cv2.rectangle(frame, (x, y),     (x+w, y+h), (0, 200, 100), 2)
        cv2.rectangle(frame, (x, y-40),  (x+w, y),   (0, 200, 100), -1)
        cv2.putText(frame, name, (x+6, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        attendance_entry = [name, timestamp]

    # Show on background or plain frame
    if imgBackground is not None:
        try:
            imgBackground[162:162+480, 55:55+640] = frame
            display = imgBackground
        except Exception:
            display = frame
    else:
        display = frame

    cv2.putText(display, "O=Attendance  Q=Quit", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    cv2.imshow("Face Attendance — O dabao", display)

    k = cv2.waitKey(1)

    if k == ord('o') and attendance_entry:
        ts       = time.time()
        date_str = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        csv_file = os.path.join(ATTENDANCE_DIR, f"Attendance_{date_str}.csv")

        speak("Attendance Le Li Gayi")

        file_exists = os.path.isfile(csv_file)
        with open(csv_file, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(COL_NAMES)
            writer.writerow(attendance_entry)

        print(f"✅ Attendance saved: {attendance_entry}  →  {csv_file}")

    elif k == ord('o') and not attendance_entry:
        print("⚠️  Koi face detect nahi hua. Camera ke samne aao.")

    if k == ord('q'):
        print("👋 Program band ho raha hai...")
        break

video.release()
cv2.destroyAllWindows()
