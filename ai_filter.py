from nudenet import NudeDetector
import config

detector = NudeDetector()


def check_image(image_path):
    """
    Returns True if image is safe.
    Returns False if image is unsafe.
    """

    try:
        result = detector.detect(image_path)

        if len(result) == 0:
            return True

        for item in result:
            score = item.get("score", 0)

            if score >= config.NUDE_CONFIDENCE_LIMIT:
                return False

        return True

    except Exception as e:
        print("AI filter error:", e)

        # Safer decision:
        # If AI filter fails, do not approve image automatically.
        return False