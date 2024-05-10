import ddddocr
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import random
import time
import os


def change(img1: Image, img2: Image, img3: Image):
    assert img1.size == img2.size == img3.size

    for i in range(img1.size[0]):
        for j in range(img1.size[1]):
            rgb1 = img1.getpixel((i, j))
            rgb2 = img2.getpixel((i, j))
            rgb3 = img3.getpixel((i, j))

            if rgb1 == rgb2 or rgb1 == rgb3:
                continue
            elif rgb2 == rgb3:
                img1.putpixel((i, j), rgb2)
    return img1


path = './images/'
files = os.listdir(path)
images = []
ocr_byte = BytesIO()
for file in files:
    if file.endswith('.jpg') and not file.endswith('result.jpg'):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                images.append(Image.open(BytesIO(f.read())))

image_base = None
image_check = None
for image in images:
    if not image_base:
        image_base = image
        continue
    if not image_check:
        image_check = image
        continue
    image_base = change(image_base, image_check, image)
    image_check = image
image_base.save('background.jpg')
