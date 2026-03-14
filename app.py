from flask import Flask
import os
import config
from routes import register_routes

app = Flask(__name__)

# Create media folders if they don't exist
os.makedirs(config.PHOTO_PATH, exist_ok=True)
os.makedirs(config.VIDEO_PATH, exist_ok=True)

# Register all APIs
register_routes(app)

if __name__ == "__main__":
    import os
    # Render assigns the port via environment variable "PORT"
    port = int(os.environ.get("PORT", 5000))
    # host="0.0.0.0" allows external access (Render/public)
    app.run(host="0.0.0.0", port=port, debug=True)