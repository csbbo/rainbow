import base64
import os

import cv2
from django.conf import settings


def get_image_dpi(name, path=settings.PHOTOS_PATH):
    image_path = os.path.join(path, name)
    high, wide, _ = cv2.imread(image_path).shape
    return f'{wide}x{high}'


# def cv2_base64(image):
#     base64_str = cv2.imencode('.jpg', image)[1].tobytes()
#     base64_str = base64.b64encode(base64_str)
#     return base64_str


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


def cartoonise(image):
    num_down = 2  # 缩减像素采样的数目
    num_bilateral = 7  # 定义双边滤波的数目
    # 用高斯金字塔降低取样
    img_color = image
    for _ in range(num_down):
        img_color = cv2.pyrDown(img_color)
    # 重复使用小的双边滤波代替一个大的滤波
    for _ in range(num_bilateral):
        img_color = cv2.bilateralFilter(img_color, d=9, sigmaColor=9, sigmaSpace=7)
    # 升采样图片到原始大小
    for _ in range(num_down):
        img_color = cv2.pyrUp(img_color)
    # 转换为灰度并且使其产生中等的模糊
    img_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    img_blur = cv2.medianBlur(img_gray, 7)
    # 检测到边缘并且增强其效果
    img_edge = cv2.adaptiveThreshold(img_blur, 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY,
                                     blockSize=9,
                                     C=2)
    # 转换回彩色图像
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
    img_cartoon = cv2.bitwise_and(img_color, img_edge)
    return img_cartoon
