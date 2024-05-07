import ddddocr
import cv2
from PIL import Image
from io import BytesIO
from simhash import Simhash


def simhash_demo(text_a, text_b):
    """
    求两文本的相似度
    :param text_a:
    :param text_b:
    :return:
    """
    a_simhash = Simhash(text_a)
    b_simhash = Simhash(text_b)
    max_hashbit = max(len(bin(a_simhash.value)), len(bin(b_simhash.value)))
    # 汉明距离
    distince = a_simhash.distance(b_simhash)
    similar = 1 - distince / max_hashbit
    return similar


from_ocr_url = "search.png"
from_url = "images.jpg"
from_array = from_url.split(".")
to_url = "result"
to_end = "." + from_array[len(from_array) - 1]
ocr = ddddocr.DdddOcr(ocr=True, show_ad=False)
det = ddddocr.DdddOcr(det=True, ocr=True, show_ad=False)

with open(from_ocr_url, 'rb') as f:
    image_ocr = f.read()
search_words = ocr.classification(image_ocr)
charset = ""
for search_word in search_words:
    charset += search_word


with open(from_url, 'rb') as f:
    image = f.read()
bboxes = det.detection(image)
print(bboxes)

im = cv2.imread(from_url)
words = []
for i, bbox in enumerate(bboxes):
    x1, y1, x2, y2 = bbox
    img = Image.open(BytesIO(image))
    img_word = img.crop(bbox)
    img_byte = BytesIO()
    img_word.save(img_byte, 'png')
    content = img_byte.getvalue()
    img_word.save(to_url + str(i) + to_end)
    # map = {}
    # for i in range(img_word.size[0]):
    #     for j in range(img_word.size[1]):
    #         rgb = img_word.getpixel((i, j))
    #         key = str(rgb[0]) + "_" + str(rgb[1]) + "_" + str(rgb[2])
    #         if map.__contains__(key):
    #             map[key] = map[key] + 1
    #         else:
    #             map[key] = 1
    #
    ocr.set_ranges(charset)
    word = ocr.classification(content, probability=True)
    max_num = 0
    max_word = ""
    for list in word['probability']:
        for i, num in enumerate(list):
            if max_num == 0 or num < max_num:
                max_num = num
                max_word = word['charsets'][i]

    words.append(word)
    # im = cv2.rectangle(im, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)

for search_word in search_words:
    max_num = 0
    max_word = ""
    for word in words:
        num = simhash_demo(search_word, word)
        print(search_word + "/t" + word + str(num))
        if max_num == 0 or num > max_num:
            max_num = num
            max_word = word

    print("_____________________________________________")

cv2.imwrite(to_url + to_end, im)
