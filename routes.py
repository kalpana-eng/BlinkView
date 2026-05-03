import os
import time
from flask import jsonify, send_from_directory, Response, request
from werkzeug.utils import secure_filename

from camera import (
    capture_photo_from_camera,
    capture_video_from_camera,
    generate_frames,
    blink_control
)

from ai_filter import check_image
import config


def register_routes(app):

    @app.route("/")
    def home():
        return jsonify({
            "message": "BlinkView Backend Running",
            "status": "success"
        })


    @app.route("/health")
    def health():
        return jsonify({
            "status": "ok",
            "service": "BlinkView Backend"
        })


    # ---------------- PHOTO CAPTURE ----------------
    @app.route("/capture/photo", methods=["POST"])
    def capture_photo():

        filename = capture_photo_from_camera()

        if filename is None:
            return jsonify({
                "status": "error",
                "message": "Camera capture failed"
            }), 500

        safe = check_image(filename)

        if not safe:
            if os.path.exists(filename):
                os.remove(filename)

            return jsonify({
                "status": "blocked",
                "message": "Image blocked by AI safety filter. File not stored."
            }), 403

        return jsonify({
            "status": "success",
            "message": "Photo saved",
            "file": filename,
            "url": "/" + filename.replace("\\", "/")
        })


    # ---------------- VIDEO CAPTURE ----------------
    @app.route("/capture/video", methods=["POST"])
    def capture_video():

        file = capture_video_from_camera()

        if file is None:
            return jsonify({
                "status": "error",
                "message": "Video capture failed"
            }), 500

        return jsonify({
            "status": "success",
            "message": "Video saved",
            "file": file,
            "url": "/" + file.replace("\\", "/")
        })


    # ---------------- FRONTEND UPLOAD IMAGE TEST ----------------
    @app.route("/upload/image", methods=["POST"])
    def upload_image():

        if "image" not in request.files:
            return jsonify({
                "status": "error",
                "message": "No image file uploaded. Use field name: image"
            }), 400

        file = request.files["image"]

        if file.filename == "":
            return jsonify({
                "status": "error",
                "message": "Empty filename"
            }), 400

        os.makedirs(config.UPLOAD_PATH, exist_ok=True)

        filename = secure_filename(file.filename)
        saved_name = str(int(time.time())) + "_" + filename
        saved_path = os.path.join(config.UPLOAD_PATH, saved_name)

        file.save(saved_path)

        safe = check_image(saved_path)

        if not safe:
            if os.path.exists(saved_path):
                os.remove(saved_path)

            return jsonify({
                "status": "blocked",
                "message": "Image blocked by AI safety filter. File not stored."
            }), 403

        return jsonify({
            "status": "success",
            "message": "Image uploaded and approved",
            "file": saved_path,
            "url": "/" + saved_path.replace("\\", "/")
        })


    # ---------------- AI FILTER ONLY ----------------
    @app.route("/filter/image", methods=["POST"])
    def filter_image():

        if "image" not in request.files:
            return jsonify({
                "status": "error",
                "message": "No image file uploaded. Use field name: image"
            }), 400

        file = request.files["image"]

        os.makedirs(config.UPLOAD_PATH, exist_ok=True)

        filename = secure_filename(file.filename)
        temp_path = os.path.join(
            config.UPLOAD_PATH,
            "temp_" + str(int(time.time())) + "_" + filename
        )

        file.save(temp_path)

        safe = check_image(temp_path)

        if os.path.exists(temp_path):
            os.remove(temp_path)

        return jsonify({
            "status": "success",
            "safe": safe,
            "message": "Safe image" if safe else "Unsafe image"
        })


    # ---------------- GALLERY ----------------
    @app.route("/gallery")
    def gallery():

        os.makedirs(config.PHOTO_PATH, exist_ok=True)
        os.makedirs(config.VIDEO_PATH, exist_ok=True)

        photos = os.listdir(config.PHOTO_PATH)
        videos = os.listdir(config.VIDEO_PATH)

        return jsonify({
            "status": "success",
            "photos": photos,
            "videos": videos
        })


    # ---------------- MEDIA SERVE ----------------
    @app.route("/media/<path:filename>")
    def media(filename):
        return send_from_directory("media", filename)


    # ---------------- UPLOAD SERVE ----------------
    @app.route("/uploads/<path:filename>")
    def uploads(filename):
        return send_from_directory("uploads", filename)


    # ---------------- LIVE CAMERA ----------------
    @app.route("/live")
    def live():
        return Response(
            generate_frames(),
            mimetype="multipart/x-mixed-replace; boundary=frame"
        )


    # ---------------- BLINK CONTROL ----------------
    @app.route("/blink-control")
    def blink():
        blink_control()

        return jsonify({
            "status": "success",
            "message": "Blink control stopped"
        })