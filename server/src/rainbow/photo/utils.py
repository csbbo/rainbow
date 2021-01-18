import base64
import os

import cv2
from django.conf import settings


def get_image_dpi(name, path=settings.PHOTOS_PATH):
    image_path = os.path.join(path, name)
    high, wide, _ = cv2.imread(image_path).shape
    return f'{wide}x{high}'


def cv2_base64(image):
    base64_str = cv2.imencode('.jpg',image)[1].tobytes()
    base64_str = base64.b64encode(base64_str)
    return base64_str
