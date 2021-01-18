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


def to_sketch(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    img_blurred = cv2.GaussianBlur(img_gray, (5, 5), 0)

    img_threshold1 = cv2.adaptiveThreshold(img_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 2)

    img_threshold1_blurred = cv2.GaussianBlur(img_threshold1, (5, 5), 0)

    _, img_threshold2 = cv2.threshold(img_threshold1_blurred, 200, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img_opening = cv2.bitwise_not(cv2.morphologyEx(cv2.bitwise_not(img_threshold2), cv2.MORPH_OPEN, kernel))

    img_opening_blurred = cv2.GaussianBlur(img_opening, (3, 3), 0)
    return img_opening_blurred
