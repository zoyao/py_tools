import ddddocr
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import random
import time


class Captcha:
    def __init__(self, is_sleep: bool = True, image_background: bytes = None):
        self.ocr = ddddocr.DdddOcr(ocr=True, show_ad=False)
        self.det = ddddocr.DdddOcr(det=True, ocr=True, show_ad=False)
        self.is_sleep = is_sleep
        self.result_image = None
        self.image_background = image_background

    def search(self, image_search: bytes, image: bytes):
        # 第一次ocr，获取指定文本
        img1 = Image.open(BytesIO(image_search))
        # 处理干扰线
        for i in range(img1.size[0]):
            for j in range(img1.size[1]):
                rgb = img1.getpixel((i, j))
                if rgb[0] == 128 and rgb[1] == 128 and rgb[2] == 128:
                    if len(rgb) == 3:
                        img1.putpixel((i, j), (0, 0, 0))
                    elif len(rgb) == 4:
                        img1.putpixel((i, j), (0, 0, 0, 255))
                else:
                    if len(rgb) == 3:
                        img1.putpixel((i, j), (255, 255, 255))
                    elif len(rgb) == 4:
                        img1.putpixel((i, j), (255, 255, 255, 255))
        for i in range(img1.size[0]):
            for j in range(img1.size[1]):
                rgb = img1.getpixel((i, j))
                if rgb[0] == 255 and rgb[1] == 255 and rgb[2] == 255:
                    if j - 1 > 0 and j + 1 < img1.size[1]:
                        rgb_up = img1.getpixel((i, j - 1))
                        rgb_down = img1.getpixel((i, j + 1))
                        if rgb != rgb_up and rgb != rgb_down and rgb_up == rgb_down:
                            img1.putpixel((i, j), rgb_up)
                            continue
        for i in range(img1.size[0]):
            for j in range(img1.size[1]):
                rgb = img1.getpixel((i, j))
                if rgb[0] == 255 and rgb[1] == 255 and rgb[2] == 255:
                    if i - 1 > 0 and i + 1 < img1.size[0]:
                        rgb_up = img1.getpixel((i - 1, j))
                        rgb_down = img1.getpixel((i + 1, j))
                        if rgb != rgb_up and rgb != rgb_down and rgb_up == rgb_down:
                            img1.putpixel((i, j), rgb_up)
        # ocr_byte = BytesIO()
        # img1.save(ocr_byte, img1.format)
        # img1.save("test.png")
        # content = ocr_byte.getvalue()
        # img1.show()
        search_words = self.ocr.classification(img1, png_fix=True)
        # 指定第三次ocr的识别范围
        self.ocr.set_ranges(search_words)

        # 处理 background
        if self.image_background:
            image_check = Image.open(BytesIO(image))
            background = Image.open(BytesIO(self.image_background))
            if image_check.size == background.size:
                for i in range(image_check.size[0]):
                    for j in range(image_check.size[1]):
                        rgb_check = image_check.getpixel((i, j))
                        rgb_bg = background.getpixel((i, j))
                        # if len(rgb_check) == 3:
                        #     image_check.putpixel((i, j), (rgb_check[0] - rgb_bg[0], rgb_check[1] - rgb_bg[1], rgb_check[2] - rgb_bg[2]))
                        # elif len(rgb_check) == 4:
                        #     image_check.putpixel((i, j), (rgb_check[0] - rgb_bg[0], rgb_check[1] - rgb_bg[1], rgb_check[2] - rgb_bg[2], rgb_check[3] - rgb_bg[3]))
                        if rgb_check == rgb_bg:
                            if len(rgb_check) == 3:
                                image_check.putpixel((i, j), (255, 255, 255))
                            elif len(rgb_check) == 4:
                                image_check.putpixel((i, j), (255, 255, 255, 0))
                bg_io = BytesIO()
                image_check.save(bg_io, image_check.format)
                # image_check.save("test.jpg")
                image = bg_io.getvalue()

        # 第二次ocr，获取图像文字区域

        bboxes = self.det.detection(image)
        nums = np.zeros((len(bboxes), len(search_words)))

        for i, bbox in enumerate(bboxes):
            img = Image.open(BytesIO(image))
            img_word = img.crop(bbox)
            img_byte = BytesIO()
            img_word.save(img_byte, 'png')
            content = img_byte.getvalue()

            # 第三次ocr，对图像文字区域进行识别，将每个概率存储在nums
            word = self.ocr.classification(content, probability=True)
            for word_i in word['probability']:
                for num_index, num in enumerate(word_i):
                    w = word['charsets'][num_index]
                    if len(w) > 0 and search_words.__contains__(w):
                        words_index = search_words.index(w)
                        if num > nums[i][words_index]:
                            nums[i][words_index] = num

        # 选取概率最大的线路
        route = np.zeros(len(search_words), dtype=int) - 1
        while route.min() < 0:
            max_num = nums.max()
            if max_num == 0:
                break
            max_wheres = np.argwhere(nums == max_num)
            for max_where in max_wheres:
                if route[max_where[1]] < 0 and not np.any(route == max_where[0]):
                    route[max_where[1]] = max_where[0]
                nums[max_where[0]][max_where[1]] = 0

        track_list = []
        begin = int(round(time.time() * 1000))
        image_np = np.frombuffer(image, dtype=np.uint8)
        self.result_image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        for i, point in enumerate(route):
            if self.is_sleep:
                time.sleep(random.randint(4, 7))
            bbox = bboxes[point]
            x1, y1, x2, y2 = bbox
            # x_ex = int((x2 - x1) * 0.3)
            # y_ex = int((y2 - y1) * 0.3)
            x = int((x1 + x2) / 2)
            y = int((y1 + y2) / 2)
            track_list.append({'x': x, 'y': y, 'type': 'click', 't': int(round(time.time() * 1000)) - begin})
            cv2.putText(self.result_image, str(i), (x, y), cv2.FONT_HERSHEY_COMPLEX, 2.0,
                        color=(0, 0, 255), thickness=2)
        img = Image.open(BytesIO(image))
        return {'track_list': track_list, 'width': img.width, 'height': img.height}

    def save_result(self, save_dir: str):
        cv2.imwrite(save_dir, self.result_image)


# with open("image.png", 'rb') as f:
#     image_png = f.read()
# with open("image.jpg", 'rb') as f:
#     image_jpg = f.read()
# with open("background.jpg", 'rb') as f:
#     image_bg = f.read()
# captcha = Captcha(False, image_bg)
# captcha.search(image_png, image_jpg)
# captcha.save_result("result.jpg")
