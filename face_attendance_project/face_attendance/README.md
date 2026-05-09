# 🎓 Face Recognition Attendance System

Real-time face recognition se automatic attendance — OpenCV + KNN + Streamlit.

## 📁 Folder Structure

```
face_attendance/
│
├── app.py                  ← Streamlit dashboard (Cloud pe deploy hoga)
├── add_faces.py            ← Face data collect karo (LOCAL only)
├── test.py                 ← Real-time recognition (LOCAL only)
│
├── requirements.txt        ← Python libraries (Cloud ke liye)
├── packages.txt            ← System libraries (Cloud ke liye)
│
├── .streamlit/
│   └── config.toml         ← Streamlit theme settings
│
├── data/
│   ├── haarcascade_frontalface_default.xml
│   ├── names.pkl           ← add_faces.py se generate hoga
│   └── faces_data.pkl      ← add_faces.py se generate hoga
│
├── Attendance/
│   └── Attendance_DD-MM-YYYY.csv   ← test.py se generate hoga
│
└── background.png          ← (Optional) camera background
```

---

## 🚀 Local Machine Pe Setup

### 1. Libraries install karein
```bash
pip install opencv-python scikit-learn numpy pandas streamlit streamlit-autorefresh pywin32
```
> Mac/Linux pe `pywin32` ki zaroorat nahi — test.py mein voice feature auto-skip ho jata hai.

### 2. data/ folder mein haarcascade daalo
```
data/haarcascade_frontalface_default.xml
```

### 3. Face data collect karein
```bash
python add_faces.py
```
- Naam daalo jab pooche
- Camera ke samne baitho — 100 samples auto-lega
- Multiple logon ke liye baar baar chalao

### 4. Attendance lein
```bash
python test.py
```
- **O** dabao → attendance save hogi
- **Q** dabao → program band karo

### 5. Dashboard dekho
```bash
streamlit run app.py
```

---

## ☁️ Streamlit Cloud Pe Deploy

1. Ye poora folder **GitHub pe push** karein
2. [share.streamlit.io](https://share.streamlit.io) pe jayen
3. Repository connect karein, `app.py` select karein
4. **Deploy!**

> **Note:** Cloud pe sirf `app.py` (dashboard) kaam karta hai.  
> `test.py` aur `add_faces.py` webcam ke liye LOCAL machine pe chalana hoga.  
> Attendance CSV sidebar se upload kar sakte hain ya Attendance/ folder mein rakh sakte hain.

---

## 🔑 Controls (test.py)
| Key | Kaam |
|-----|------|
| `O` | Attendance save karo |
| `Q` | Program band karo |
