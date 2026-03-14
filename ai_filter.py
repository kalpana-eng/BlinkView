from nudenet import NudeDetector

detector = NudeDetector()

def check_image(image_path):

    result = detector.detect(image_path)

    # if nothing detected → safe
    if len(result) == 0:
        return True

    # check confidence
    for item in result:
        score = item['score']

        if score > 0.7:   # strong detection
            return False

    return True