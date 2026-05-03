# BlinkView Backend Handover Document

## 1. Project Overview

BlinkView is an AI-based smart glass backend system. The purpose of this backend is to support a wearable smart glass device that can capture photos and videos using eye blink gestures.

The system is designed with the following main features:

- Live camera feed
- Intentional blink detection
- Single intentional blink to capture photo
- Double intentional blink to capture video
- Natural blink ignore logic
- AI safety filter to block unsafe/nude images
- Media gallery API
- Frontend API support
- Local device testing support
- Cloud testing support for upload/filter APIs

This backend is built using Python Flask and computer vision libraries.

---

## 2. Main Concept of the Project

The main concept of BlinkView is:

```text
Smart Glass Camera
        ↓
Backend reads camera feed
        ↓
MediaPipe detects face and eye landmarks
        ↓
Backend detects blink duration
        ↓
Natural blink is ignored
        ↓
Intentional blink triggers action
        ↓
Single intentional blink captures photo
Double intentional blink captures video
        ↓
AI filter checks image safety
        ↓
Safe media is stored
Unsafe media is blocked
```

---

## 3. Important Blink Logic

The backend separates natural blink and intentional blink.

### Natural Blink

Natural blink is usually very fast.

Current logic:

```text
If blink duration is less than or equal to NATURAL_BLINK_MAX_DURATION,
then it is treated as natural blink and ignored.
```

### Intentional Blink

Intentional blink is held for a longer duration.

Current logic:

```text
If blink duration is greater than or equal to INTENTIONAL_BLINK_MIN_DURATION,
then it is treated as intentional blink.
```

### Single Blink Action

```text
One intentional blink → Capture photo
```

### Double Blink Action

```text
Two intentional blinks within DOUBLE_BLINK_WINDOW → Capture video
```

---

## 4. Current Configuration

The configuration is available in `config.py`.

```python
PHOTO_PATH = "media/photos"
VIDEO_PATH = "media/videos"
UPLOAD_PATH = "uploads"

VIDEO_DURATION = 10
CAMERA_ID = 0

NATURAL_BLINK_MAX_DURATION = 0.35
INTENTIONAL_BLINK_MIN_DURATION = 0.55
DOUBLE_BLINK_WINDOW = 2.0

NUDE_CONFIDENCE_LIMIT = 0.7
```

### Meaning of Configuration

| Config | Meaning |
|---|---|
| `PHOTO_PATH` | Folder where captured photos are saved |
| `VIDEO_PATH` | Folder where captured videos are saved |
| `UPLOAD_PATH` | Folder for uploaded images during API testing |
| `VIDEO_DURATION` | Duration of captured video in seconds |
| `CAMERA_ID` | Camera index. Usually `0` means default camera |
| `NATURAL_BLINK_MAX_DURATION` | Maximum duration for natural blink |
| `INTENTIONAL_BLINK_MIN_DURATION` | Minimum duration for intentional blink |
| `DOUBLE_BLINK_WINDOW` | Time window for double blink detection |
| `NUDE_CONFIDENCE_LIMIT` | AI confidence threshold for blocking unsafe image |

---

## 5. Tech Stack

The backend uses the following technologies:

| Technology | Purpose |
|---|---|
| Python | Main backend language |
| Flask | API server |
| Flask-CORS | Allows frontend to connect with backend |
| OpenCV | Camera access, frame reading, photo/video capture |
| MediaPipe | Face mesh and eye landmark detection |
| NudeNet | AI-based unsafe/nude image detection |
| ONNXRuntime | Required by NudeNet model execution |
| Pillow | Image processing support |
| Gunicorn | Production server for deployment |
| NumPy | Numerical processing used by computer vision libraries |

---

## 6. Installed Dependencies

The dependencies are stored in `requirements.txt`.

```txt
Flask==3.1.0
flask-cors==5.0.1
numpy==1.26.4
opencv-python==4.10.0.84
mediapipe==0.10.14
nudenet==3.4.2
onnxruntime==1.23.2
Pillow==11.2.1
gunicorn==22.0.0
```

### Why These Versions Are Used

| Package | Version | Reason |
|---|---:|---|
| Flask | 3.1.0 | Flask backend API |
| flask-cors | 5.0.1 | Frontend integration |
| numpy | 1.26.4 | Stable version compatible with OpenCV/MediaPipe |
| opencv-python | 4.10.0.84 | Required for camera access and `cv2.imshow()` |
| mediapipe | 0.10.14 | Supports `mp.solutions.face_mesh` |
| nudenet | 3.4.2 | AI safety/nude image detection |
| onnxruntime | 1.23.2 | NudeNet model runtime |
| Pillow | 11.2.1 | Image processing support |
| gunicorn | 22.0.0 | Required for cloud/production deployment |

---

## 7. Important Fixes Done

### 7.1 MediaPipe Issue Fixed

Earlier error:

```text
AttributeError: module 'mediapipe' has no attribute 'solutions'
```

Reason:

Newer MediaPipe versions may not support old `mp.solutions.face_mesh` structure properly.

Fix:

```txt
mediapipe==0.10.14
```

---

### 7.2 OpenCV Headless Issue Fixed

Earlier dependency had:

```txt
opencv-python-headless
```

But the backend uses:

```python
cv2.imshow()
```

`opencv-python-headless` does not support GUI/camera window properly.

Fix:

```txt
opencv-python==4.10.0.84
```

---

### 7.3 NumPy Compatibility Fixed

Earlier NumPy version was:

```txt
numpy==2.1.3
```

Some computer vision libraries may create compatibility issues with NumPy 2.x.

Fix:

```txt
numpy==1.26.4
```

---

### 7.4 CORS Added

Frontend needs to call backend APIs from another port or domain.

Fix added in `app.py`:

```python
from flask_cors import CORS
CORS(app)
```

---

### 7.5 Upload Folder Added

For frontend and cloud testing, upload folder support was added.

```python
os.makedirs(config.UPLOAD_PATH, exist_ok=True)
```

---

### 7.6 AI Filter Improved

Earlier AI filter was basic.

Now:

- If image is safe, backend allows it.
- If unsafe/nude content is detected above threshold, backend blocks it.
- If AI filter fails, backend blocks the image for safety.

Logic:

```text
Safe image → save/approve
Unsafe image → block and delete
AI filter error → block
```

---

### 7.7 GitHub Cleanup Done

The following files/folders should not be pushed to GitHub:

```text
venv/
__pycache__/
*.pyc
media/photos/*
media/videos/*
uploads/*
.env
ngrok.exe
```

These are ignored using `.gitignore`.

---

## 8. Project File Structure

```text
BlinkView/
│
├── app.py
├── camera.py
├── routes.py
├── config.py
├── ai_filter.py
├── bluetooth_notify.py
├── requirements.txt
├── requirements-local.txt
├── README.txt
├── HANDOVER.md
├── .gitignore
│
├── media/
│   ├── photos/
│   └── videos/
│
├── uploads/
│
└── venv/
```

### File Responsibilities

| File | Purpose |
|---|---|
| `app.py` | Flask application entry point |
| `camera.py` | Camera, live feed, photo/video capture, blink detection |
| `routes.py` | API endpoints |
| `config.py` | Project settings and thresholds |
| `ai_filter.py` | AI safety filter using NudeNet |
| `bluetooth_notify.py` | Optional Bluetooth notification logic |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Prevents unwanted files from being pushed |
| `media/photos` | Stores captured photos locally |
| `media/videos` | Stores captured videos locally |
| `uploads` | Stores uploaded files temporarily |

---

## 9. Local Setup Instructions

### Step 1: Clone Repository

```bash
git clone https://github.com/kalpana-eng/BlinkView.git
```

### Step 2: Go Inside Project Folder

```bash
cd BlinkView
```

### Step 3: Create Virtual Environment

```bash
python -m venv venv
```

If `python` does not work, try:

```bash
py -m venv venv
```

### Step 4: Activate Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If execution policy error comes, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then again run:

```powershell
.\venv\Scripts\Activate.ps1
```

After activation, terminal should show:

```text
(venv)
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run Backend

```bash
python app.py
```

Expected output:

```text
Running on http://127.0.0.1:5000
Running on http://YOUR_LOCAL_IP:5000
```

Example:

```text
Running on http://192.168.1.3:5000
```

---

## 10. Backend URLs

### Local Machine URL

```text
http://127.0.0.1:5000
```

### Same Wi-Fi Testing URL

Use system IP address.

Example:

```text
http://192.168.1.3:5000
```

Team members connected to the same Wi-Fi can test using:

```text
http://192.168.1.3:5000/health
```

---

## 11. API Endpoints

| Method | Endpoint | Purpose | Camera Required |
|---|---|---|---|
| GET | `/` | Root backend check | No |
| GET | `/health` | Health check | No |
| GET | `/live` | Live camera feed | Yes |
| POST | `/capture/photo` | Manual photo capture | Yes |
| POST | `/capture/video` | Manual video capture | Yes |
| GET | `/blink-control` | Start blink detection | Yes |
| GET | `/gallery` | List saved photos/videos | No |
| GET | `/media/photos/<filename>` | View saved photo | No |
| GET | `/media/videos/<filename>` | View saved video | No |
| POST | `/upload/image` | Upload image and apply AI safety filter | No |
| POST | `/filter/image` | Test AI safety filter only | No |

---

## 12. API Testing Instructions

### 12.1 Test Root API

Open in browser:

```text
http://127.0.0.1:5000/
```

Expected response:

```json
{
  "message": "BlinkView Backend Running",
  "status": "success"
}
```

---

### 12.2 Test Health API

Open in browser:

```text
http://127.0.0.1:5000/health
```

Expected response:

```json
{
  "service": "BlinkView Backend",
  "status": "ok"
}
```

---

### 12.3 Test Live Camera Feed

Open in browser:

```text
http://127.0.0.1:5000/live
```

Expected result:

```text
Live camera feed should appear in browser.
```

Important:

```text
/live only shows camera feed. It does not detect blink.
```

---

### 12.4 Test Manual Photo Capture

Use PowerShell:

```powershell
curl -X POST http://127.0.0.1:5000/capture/photo
```

Expected result:

```json
{
  "status": "success",
  "message": "Photo saved",
  "file": "media/photos/photo_xxxxx.jpg",
  "url": "/media/photos/photo_xxxxx.jpg"
}
```

Saved file location:

```text
media/photos/
```

---

### 12.5 Test Manual Video Capture

Use PowerShell:

```powershell
curl -X POST http://127.0.0.1:5000/capture/video
```

Expected result:

```json
{
  "status": "success",
  "message": "Video saved",
  "file": "media/videos/video_xxxxx.avi",
  "url": "/media/videos/video_xxxxx.avi"
}
```

Saved file location:

```text
media/videos/
```

---

### 12.6 Test Gallery API

Open in browser:

```text
http://127.0.0.1:5000/gallery
```

Expected result:

```json
{
  "status": "success",
  "photos": [],
  "videos": []
}
```

If photos/videos are already captured, filenames will be shown in the list.

---

### 12.7 Test Saved Media

If gallery returns:

```json
{
  "photos": ["photo_123.jpg"]
}
```

Open:

```text
http://127.0.0.1:5000/media/photos/photo_123.jpg
```

If gallery returns:

```json
{
  "videos": ["video_123.avi"]
}
```

Open:

```text
http://127.0.0.1:5000/media/videos/video_123.avi
```

---

### 12.8 Test Blink Control

Close `/live` tab first because the camera may be busy.

Then open:

```text
http://127.0.0.1:5000/blink-control
```

Expected behavior:

```text
A camera window opens.
Natural blink is ignored.
Long single blink captures photo.
Two long blinks capture video.
Press ESC to stop.
```

Important:

```text
/blink-control runs a continuous loop.
Browser may keep loading until the blink window is closed.
```

---

### 12.9 Test Upload Image API

This is useful for frontend and cloud testing.

Frontend form field name must be:

```text
image
```

Example JavaScript:

```js
const formData = new FormData();
formData.append("image", selectedFile);

fetch("http://127.0.0.1:5000/upload/image", {
  method: "POST",
  body: formData
})
  .then(res => res.json())
  .then(data => console.log(data));
```

Expected safe image response:

```json
{
  "status": "success",
  "message": "Image uploaded and approved",
  "file": "uploads/xxxxx.jpg",
  "url": "/uploads/xxxxx.jpg"
}
```

Expected unsafe image response:

```json
{
  "status": "blocked",
  "message": "Image blocked by AI safety filter. File not stored."
}
```

---

### 12.10 Test AI Filter Only API

Example JavaScript:

```js
const formData = new FormData();
formData.append("image", selectedFile);

fetch("http://127.0.0.1:5000/filter/image", {
  method: "POST",
  body: formData
})
  .then(res => res.json())
  .then(data => console.log(data));
```

Expected response:

```json
{
  "status": "success",
  "safe": true,
  "message": "Safe image"
}
```

Or:

```json
{
  "status": "success",
  "safe": false,
  "message": "Unsafe image"
}
```

Important:

```text
/filter/image checks the image and deletes temporary uploaded file after checking.
```

---

## 13. Frontend Integration Examples

### Health Check

```js
fetch("http://127.0.0.1:5000/health")
  .then(res => res.json())
  .then(data => console.log(data));
```

### Live Feed

```html
<img src="http://127.0.0.1:5000/live" />
```

### Capture Photo

```js
fetch("http://127.0.0.1:5000/capture/photo", {
  method: "POST"
})
  .then(res => res.json())
  .then(data => console.log(data));
```

### Capture Video

```js
fetch("http://127.0.0.1:5000/capture/video", {
  method: "POST"
})
  .then(res => res.json())
  .then(data => console.log(data));
```

### Gallery

```js
fetch("http://127.0.0.1:5000/gallery")
  .then(res => res.json())
  .then(data => console.log(data));
```

### Show Photo From Gallery

```html
<img src="http://127.0.0.1:5000/media/photos/photo_123.jpg" />
```

### Upload Image for AI Filtering

```js
const formData = new FormData();
formData.append("image", selectedFile);

fetch("http://127.0.0.1:5000/upload/image", {
  method: "POST",
  body: formData
})
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## 14. Local Testing Flow for Team

The team should test in this order:

### Test 1: Backend Start

```bash
python app.py
```

### Test 2: Health Check

```text
http://127.0.0.1:5000/health
```

### Test 3: Live Camera

```text
http://127.0.0.1:5000/live
```

### Test 4: Manual Photo

```powershell
curl -X POST http://127.0.0.1:5000/capture/photo
```

### Test 5: Manual Video

```powershell
curl -X POST http://127.0.0.1:5000/capture/video
```

### Test 6: Gallery

```text
http://127.0.0.1:5000/gallery
```

### Test 7: Blink Control

```text
http://127.0.0.1:5000/blink-control
```

### Test 8: Upload Image AI Filter

Use frontend upload or Postman with form-data:

```text
key: image
type: file
value: select image file
```

Endpoint:

```text
POST http://127.0.0.1:5000/upload/image
```

---

## 15. Postman Testing

Use Postman for API testing.

### For Photo Capture

Method:

```text
POST
```

URL:

```text
http://127.0.0.1:5000/capture/photo
```

Body:

```text
No body required
```

### For Video Capture

Method:

```text
POST
```

URL:

```text
http://127.0.0.1:5000/capture/video
```

Body:

```text
No body required
```

### For Image Upload

Method:

```text
POST
```

URL:

```text
http://127.0.0.1:5000/upload/image
```

Body:

```text
form-data
key: image
type: File
value: select image
```

---

## 16. Cloud Deployment Important Note

Cloud deployment can be used only for APIs that do not require physical camera access.

### Works on Cloud

```text
/health
/upload/image
/filter/image
/gallery
```

### Does Not Work Properly on Cloud

```text
/live
/capture/photo
/capture/video
/blink-control
```

Reason:

```text
Cloud servers like Render, Railway, AWS, etc. cannot access the physical camera of a laptop or smart glass.
```

For real smart glass use case, backend should run on the physical device or edge device.

Example:

```text
Smart Glass / Raspberry Pi / Local Laptop → runs Flask backend
Frontend / Mobile App → connects to backend IP
```

---

## 17. Recommended Deployment Modes

### Mode 1: Local Smart Glass Mode

Use this for actual camera and blink detection.

```text
Backend runs on smart glass device or laptop.
Frontend connects using local IP.
```

Example:

```text
http://192.168.1.3:5000
```

### Mode 2: Cloud Testing Mode

Use this for frontend team testing of upload and AI filter.

```text
Backend runs on Render/Railway.
Camera features disabled or not used.
Frontend tests /upload/image and /filter/image.
```

### Mode 3: Temporary Remote Testing Using ngrok

Use this only when local backend is running and laptop is ON.

Command:

```bash
ngrok http 5000
```

ngrok gives a public HTTPS URL.

Example:

```text
https://example-ngrok-url.ngrok-free.app
```

Frontend can use:

```text
https://example-ngrok-url.ngrok-free.app/health
```

Important:

```text
If laptop is off, ngrok URL will stop working.
Free ngrok URL may change after restart.
```

---

## 18. Known Limitations

1. `/live` only shows camera feed.
2. `/live` does not currently trigger blink capture.
3. `/blink-control` opens an OpenCV window and handles blink detection.
4. Camera can be used by only one active process at a time.
5. If `/live` is open, `/blink-control` may not get camera access.
6. Cloud deployment cannot access local camera.
7. NudeNet detection depends on model confidence and may need threshold tuning.
8. Blink detection threshold may need tuning depending on camera quality, lighting, and user distance.
9. Bluetooth file is currently optional and not connected to main API flow.

---

## 19. Troubleshooting

### Problem: `mediapipe has no attribute solutions`

Fix:

```bash
pip uninstall mediapipe -y
pip install mediapipe==0.10.14
```

### Problem: Camera not opening

Check:

```python
CAMERA_ID = 0
```

Try changing to:

```python
CAMERA_ID = 1
```

Also close Zoom, Teams, browser camera tabs, or any app using camera.

### Problem: `/live` works but blink does not capture

Reason:

```text
/live only streams camera feed.
Blink capture happens from /blink-control.
```

Use:

```text
http://127.0.0.1:5000/blink-control
```

### Problem: `/blink-control` not working

Close `/live` tab first.

Then restart backend:

```bash
CTRL + C
python app.py
```

Then open:

```text
http://127.0.0.1:5000/blink-control
```

### Problem: Image blocked even when safe

Possible reasons:

```text
AI confidence threshold too strict.
Model error occurred.
Image quality is poor.
```

Check:

```python
NUDE_CONFIDENCE_LIMIT = 0.7
```

Can tune to:

```python
NUDE_CONFIDENCE_LIMIT = 0.8
```

### Problem: Frontend cannot connect

Check:

1. Backend running or not.
2. Correct URL used or not.
3. CORS enabled or not.
4. Same Wi-Fi connection if using local IP.
5. Firewall may block port 5000.

### Problem: Same Wi-Fi device cannot open backend

Try allowing port 5000 in Windows Firewall.

Also confirm backend is running on:

```text
0.0.0.0
```

In `app.py`:

```python
app.run(host="0.0.0.0", port=port, debug=True)
```

---

## 20. GitHub Notes

The project is pushed to:

```text
https://github.com/kalpana-eng/BlinkView
```

Do not push these files/folders:

```text
venv/
__pycache__/
*.pyc
media/photos/*
media/videos/*
uploads/*
.env
ngrok.exe
```

These are ignored using `.gitignore`.

---

## 21. Commands for Future Updates

After making code changes:

```bash
git status
git add .
git commit -m "Your update message"
git push origin main
```

Before pushing, always check that `venv`, `__pycache__`, and captured media are not being added.

---

## 22. Final Handover Summary

BlinkView backend is ready for local smart glass testing and frontend integration.

Current working features:

- Flask backend running
- Health check API working
- Live camera feed working
- Manual photo capture API
- Manual video capture API
- Gallery API
- Media serving API
- Upload image API
- AI safety filter API
- Blink detection logic for intentional blink
- Natural blink ignore logic
- Single blink photo trigger
- Double blink video trigger

Important final note:

```text
For real smart glass/camera features, backend must run on the physical device.
For cloud testing, use only upload/filter/gallery APIs.
```

---

## 23. Project Backend developer
Kalpana Kumari



 current project 
 we would say bcz its working with web cam 
 BlinkView Prototype Mode

 features
 /life or /live = camera feed
/capture/photo = photo capture
/capture/video = video capture
/blink-control = blink detection
/gallery = saved media list
/upload/image = AI filter test
/filter/image = AI safety check