# BlinkView Project

## Overview
**BlinkView** is a smart AI-powered camera system that detects **blinks** and triggers **photo or video capture** automatically. It also provides:

- Live camera feed streaming  
- Photo & video capture via API  
- AI-based safety filter to block inappropriate images  
- Media gallery API  
- Optional blink-controlled capture (single/double blink)

This README covers setup, backend structure, API usage, and sharing with your team.

---

## Features

1. **Blink Detection**  
   - Single blink → Capture photo  
   - Double blink → Capture video  

2. **Live Camera Feed**  
   - MJPEG streaming via `/live` endpoint  

3. **Media Management**  
   - Capture photos/videos  
   - View gallery of saved media  
   - Serve individual media files  

4. **AI Filter**  
   - Uses `NudeDetector` to block unsafe images before saving  

5. **Remote Access**  
   - Expose backend via ngrok for team access  
   - Temporary public URL for development/testing  

---

## Project Structure

blinkview_project/
│
├── app.py # Flask server entry point
├── camera.py # Blink detection, photo/video capture
├── routes.py # Flask API endpoints
├── config.py # Media paths and camera settings
├── ai_filter.py # AI-based image safety filter
├── media/ # Folder for saved media
│ ├── photos/
│ └── videos/
├── README.md # Project instructions
└── ngrok.exe # ngrok executable for public endpoint (optional)


---

## Requirements

- Python 3.10+  
- Flask  
- OpenCV (`cv2`)  
- MediaPipe (`mediapipe`)  
- NudeNet (`nudenet`)  
- ngrok (for remote access)

Install dependencies:

```bash
pip install flask opencv-python mediapipe nudenet

