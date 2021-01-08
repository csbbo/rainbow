import os

import cv2
from django.conf import settings


def get_image_dpi(name, path=settings.PHOTOS_PATH):
    image_path = os.path.join(path, name)
    high, wide, _ = cv2.imread(image_path).shape
    return f'{wide}x{high}'
