'''PHOTO_PATH = "media/photos"
VIDEO_PATH = "media/videos"
UPLOAD_PATH = "uploads"

VIDEO_DURATION = 10  # seconds
CAMERA_ID = 0

# Blink logic
NATURAL_BLINK_MAX_DURATION = 0.35
INTENTIONAL_BLINK_MIN_DURATION = 0.55
DOUBLE_BLINK_WINDOW = 2.0

# AI safety filter
NUDE_CONFIDENCE_LIMIT = 0.7'''

import os

PHOTO_PATH = "media/photos"
VIDEO_PATH = "media/videos"
UPLOAD_PATH = "uploads"

VIDEO_DURATION = 10  # seconds
CAMERA_ID = 0

# Deployment mode
CLOUD_MODE = os.environ.get("CLOUD_MODE", "false").lower() == "true"

# Blink logic
NATURAL_BLINK_MAX_DURATION = 0.35
INTENTIONAL_BLINK_MIN_DURATION = 0.55
DOUBLE_BLINK_WINDOW = 2.0

# AI safety filter
NUDE_CONFIDENCE_LIMIT = 0.7