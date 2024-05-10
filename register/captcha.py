import ddddocr
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import random
import time


class Captcha:
    def __init__(self, is_sleep=True):
        self.ocr = ddddocr.DdddOcr(ocr=True, show_ad=False)
        self.det = ddddocr.DdddOcr(det=True, ocr=True, show_ad=False)
        self.is_sleep = is_sleep
        self.result_image = None

    def search(self, image_search, image):
        # 第一次ocr，获取指定文本
        ocr_byte = BytesIO()
        img1 = Image.open(BytesIO(image_search))
        # 处理干扰线
        for i in range(img1.size[0]):
            for j in range(img1.size[1]):
                rgb = img1.getpixel((i, j))
                if rgb[0] == 128 and rgb[1] == 128 and rgb[2] == 128:
                    img1.putpixel((i, j), (0, 0, 0, 255))
                else:
                    img1.putpixel((i, j), (255, 255, 255, 255))
        img1.save(ocr_byte, 'png')
        content = ocr_byte.getvalue()
        search_words = self.ocr.classification(content, png_fix=True)
        # 指定第三次ocr的识别范围
        self.ocr.set_ranges(search_words)

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
            x_ex = int((x2 - x1) * 0.3)
            y_ex = int((y2 - y1) * 0.3)
            x = random.randint(x1 + x_ex, x2 - x_ex)
            y = random.randint(y1 + y_ex, y2 - y_ex)
            track_list.append({'x': x, 'y': y, 'type': 'click', 't': int(round(time.time() * 1000)) - begin})
            cv2.putText(self.result_image, str(i), (x, y), cv2.FONT_HERSHEY_COMPLEX, 2.0,
                        color=(0, 0, 255), thickness=2)
        img = Image.open(BytesIO(image))
        return {'track_list': track_list, 'width': img.width, 'height': img.height}

    def save_result(self, save_dir):
        cv2.imwrite(save_dir, self.result_image)


# with open("image.png", 'rb') as f:
#     image_png = f.read()
# with open("image.jpg", 'rb') as f:
#     image_jpg = f.read()
# captcha = Captcha(False)
# captcha.search_track_list(image_png, image_jpg)
# captcha.save_result("result.jpg")
