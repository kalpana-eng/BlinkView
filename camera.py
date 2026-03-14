import cv2
import time
import mediapipe as mp
import os
import config

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

# ---------------- PHOTO CAPTURE ----------------
def capture_photo_from_camera():
    cap = cv2.VideoCapture(config.CAMERA_ID)
    ret, frame = cap.read()

    if not ret:
        cap.release()
        return None

    os.makedirs(config.PHOTO_PATH, exist_ok=True)
    filename = os.path.join(config.PHOTO_PATH, "photo_" + str(int(time.time())) + ".jpg")
    cv2.imwrite(filename, frame)
    cap.release()
    print("Photo saved:", filename)
    return filename

# ---------------- VIDEO CAPTURE ----------------
def capture_video_from_camera():
    cap = cv2.VideoCapture(config.CAMERA_ID)
    os.makedirs(config.VIDEO_PATH, exist_ok=True)
    filename = os.path.join(config.VIDEO_PATH, "video_" + str(int(time.time())) + ".avi")

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    start = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        out.write(frame)

        if time.time() - start > config.VIDEO_DURATION:
            break

    cap.release()
    out.release()
    print("Video saved:", filename)
    return filename

# ---------------- BLINK CONTROL ----------------
def blink_control():
    cap = cv2.VideoCapture(config.CAMERA_ID)

    blink_count = 0
    last_blink_time = 0
    blink_start_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]

            top = face_landmarks.landmark[159].y
            bottom = face_landmarks.landmark[145].y
            eye_distance = abs(top - bottom)
            current_time = time.time()

            if current_time - blink_start_time > 2:
                blink_count = 0

            if eye_distance < 0.02:
                if current_time - last_blink_time > 0.8:
                    blink_count += 1
                    last_blink_time = current_time
                    blink_start_time = current_time

                    print("Blink detected:", blink_count)

                    if blink_count == 1:
                        print("Single Blink → Photo")
                        capture_photo_from_camera()

                    elif blink_count == 2:
                        print("Double Blink → Video")
                        capture_video_from_camera()
                        blink_count = 0

        cv2.imshow("BlinkView Camera", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

# ---------------- LIVE CAMERA FRAMES ----------------
def generate_frames():
    cap = cv2.VideoCapture(config.CAMERA_ID)

    while True:
        success, frame = cap.read()
        if not success:
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')