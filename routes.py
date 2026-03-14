import os
from flask import jsonify, send_from_directory, Response
from camera import capture_photo_from_camera, capture_video_from_camera

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
        return "BlinkView Backend Running"


    # ---------------- PHOTO CAPTURE ----------------
    @app.route("/capture/photo", methods=["POST"])
    def capture_photo():

        filename = capture_photo_from_camera()

        if filename is None:
            return jsonify({"error": "Camera capture failed"})

        safe = check_image(filename)

        if not safe:
            os.remove(filename)
            return jsonify({
                "message": "Image blocked by AI"
            })

        return jsonify({
            "message": "Photo saved",
            "file": filename
        })


    # ---------------- VIDEO CAPTURE ----------------
    @app.route("/capture/video", methods=["POST"])
    def video():

        file = capture_video_from_camera()

        if file is None:
            return jsonify({"error": "Video capture failed"})

        return jsonify({
            "message": "Video saved",
            "file": file
        })


    # ---------------- GALLERY ----------------
    @app.route("/gallery")
    def gallery():

        photos = os.listdir(config.PHOTO_PATH)
        videos = os.listdir(config.VIDEO_PATH)

        return jsonify({
            "photos": photos,
            "videos": videos
        })


    # ---------------- MEDIA SERVE ----------------
    @app.route("/media/<path:filename>")
    def media(filename):

        return send_from_directory("media", filename)


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

        return "Blink control started"