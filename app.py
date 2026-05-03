from flask import Flask
from flask_cors import CORS
import os
import config
from routes import register_routes

app = Flask(__name__)
CORS(app)

# Create required folders
os.makedirs(config.PHOTO_PATH, exist_ok=True)
os.makedirs(config.VIDEO_PATH, exist_ok=True)
os.makedirs(config.UPLOAD_PATH, exist_ok=True)

# Register routes
register_routes(app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )