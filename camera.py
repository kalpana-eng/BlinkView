import cv2
import time
import mediapipe as mp
import os
import config

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# ---------------- PHOTO CAPTURE ----------------
def capture_photo_from_camera():
    cap = cv2.VideoCapture(config.CAMERA_ID)

    if not cap.isOpened():
        print("Camera not opened")
        return None

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Photo capture failed")
        return None

    os.makedirs(config.PHOTO_PATH, exist_ok=True)

    filename = os.path.join(
        config.PHOTO_PATH,
        "photo_" + str(int(time.time())) + ".jpg"
    )

    cv2.imwrite(filename, frame)
    print("Photo saved:", filename)

    return filename


# ---------------- VIDEO CAPTURE ----------------
def capture_video_from_camera():
    cap = cv2.VideoCapture(config.CAMERA_ID)

    if not cap.isOpened():
        print("Camera not opened")
        return None

    os.makedirs(config.VIDEO_PATH, exist_ok=True)

    filename = os.path.join(
        config.VIDEO_PATH,
        "video_" + str(int(time.time())) + ".avi"
    )

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(filename, fourcc, 20.0, (width, height))

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


# ---------------- EYE DISTANCE ----------------
def get_eye_distance(face_landmarks):
    top = face_landmarks.landmark[159].y
    bottom = face_landmarks.landmark[145].y

    return abs(top - bottom)


# ---------------- BLINK CONTROL ----------------
def blink_control():
    cap = cv2.VideoCapture(config.CAMERA_ID)

    if not cap.isOpened():
        print("Camera not opened")
        return

    intentional_blinks = []
    eye_closed = False
    blink_start_time = None

    print("Blink control started. Press ESC to stop.")

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        current_time = time.time()

        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            eye_distance = get_eye_distance(face_landmarks)

            # Eye closed
            if eye_distance < 0.02 and not eye_closed:
                eye_closed = True
                blink_start_time = current_time

            # Eye opened again
            elif eye_distance >= 0.02 and eye_closed:
                eye_closed = False

                blink_duration = current_time - blink_start_time

                print("Blink duration:", round(blink_duration, 2), "seconds")

                # Ignore natural blink
                if blink_duration <= config.NATURAL_BLINK_MAX_DURATION:
                    print("Natural blink ignored")

                # Intentional blink
                elif blink_duration >= config.INTENTIONAL_BLINK_MIN_DURATION:
                    print("Intentional blink detected")

                    intentional_blinks.append(current_time)

                    # Remove old blinks
                    intentional_blinks = [
                        t for t in intentional_blinks
                        if current_time - t <= config.DOUBLE_BLINK_WINDOW
                    ]

                    if len(intentional_blinks) == 1:
                        print("Single intentional blink → Photo")
                        capture_photo_from_camera()

                    elif len(intentional_blinks) >= 2:
                        print("Double intentional blink → Video")
                        capture_video_from_camera()
                        intentional_blinks = []

        cv2.imshow("BlinkView Camera", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


# ---------------- LIVE CAMERA FRAMES ----------------
def generate_frames():
    cap = cv2.VideoCapture(config.CAMERA_ID)

    if not cap.isOpened():
        print("Camera not opened")
        return

    while True:
        success, frame = cap.read()

        if not success:
            break

        ret, buffer = cv2.imencode(".jpg", frame)

        if not ret:
            continue

        frame = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )

    cap.release()