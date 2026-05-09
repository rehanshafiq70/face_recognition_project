"""
add_faces.py  —  LOCAL MACHINE PE CHALAO (webcam chahiye)
Ye script cloud pe kaam nahi karti.
"""

import cv2
import pickle
import numpy as np
import os

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

video = cv2.VideoCapture(0)
if not video.isOpened():
    print("❌ Camera nahi khula. Check karein camera connected hai ya nahi.")
    exit()

facedetect = cv2.CascadeClassifier(os.path.join(DATA_DIR, "haarcascade_frontalface_default.xml"))

name = input("Enter Your Name: ").strip()
if not name:
    print("❌ Naam khaali nahi ho sakta.")
    exit()

faces_data = []
i = 0
SAMPLE_COUNT = 100

print(f"✅ '{name}' ke liye {SAMPLE_COUNT} samples liye ja rahe hain...")
print("   Camera ke samne baitho. 'Q' dabao band karne ke liye.")

while True:
    ret, frame = video.read()
    if not ret:
        print("❌ Frame nahi mila.")
        break

    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        crop_img    = frame[y:y+h, x:x+w]
        resized_img = cv2.resize(crop_img, (50, 50))
        if len(faces_data) < SAMPLE_COUNT and i % 10 == 0:
            faces_data.append(resized_img)
        i += 1

        progress = len(faces_data)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 200, 100), 2)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (0, 200, 100), -1)
        cv2.putText(frame, f"{name}  [{progress}/{SAMPLE_COUNT}]",
                    (x+5, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

    cv2.putText(frame, f"Samples: {len(faces_data)}/{SAMPLE_COUNT}",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,200,100), 2)
    cv2.imshow("Add Face — Q dabao band karne ke liye", frame)

    k = cv2.waitKey(1)
    if k == ord('q') or len(faces_data) >= SAMPLE_COUNT:
        break

video.release()
cv2.destroyAllWindows()

if len(faces_data) == 0:
    print("❌ Koi face detect nahi hua. Dobara try karein.")
    exit()

# ── Save data ──────────────────────────────────────────────────────────────────
faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(len(faces_data), -1)

# names.pkl
names_path = os.path.join(DATA_DIR, "names.pkl")
if os.path.exists(names_path):
    with open(names_path, "rb") as f:
        names = pickle.load(f)
    names = names + [name] * len(faces_data)
else:
    names = [name] * len(faces_data)
with open(names_path, "wb") as f:
    pickle.dump(names, f)

# faces_data.pkl
faces_path = os.path.join(DATA_DIR, "faces_data.pkl")
if os.path.exists(faces_path):
    with open(faces_path, "rb") as f:
        existing = pickle.load(f)
    faces_data = np.append(existing, faces_data, axis=0)
with open(faces_path, "wb") as f:
    pickle.dump(faces_data, f)

print(f"✅ '{name}' ka data save ho gaya! Total samples: {faces_data.shape[0]}")
print(f"   Files: {names_path} | {faces_path}")
