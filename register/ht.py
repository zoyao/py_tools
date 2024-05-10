import base64
import requests
import json
import time
import random
from faker import Faker
from Crypto.Cipher import AES
from captcha import Captcha


def pkcs7padding(text):
    """明文使用PKCS7填充 """
    bs = 16
    length = len(text)
    bytes_length = len(text.encode('utf-8'))
    padding_size = length if (bytes_length == length) else bytes_length
    padding = bs - padding_size % bs
    padding_text = chr(padding) * padding
    return text + padding_text


def aes_encrypt(data, key):
    """ AES加密 """
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    # 处理明文
    content_padding = pkcs7padding(data)
    # 加密
    encrypt_bytes = cipher.encrypt(content_padding.encode('utf-8'))
    # 重新编码
    result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
    return result


fake = Faker("zh_CN")
headers = {
    "Content-Type": "application/json"
}
captcha = Captcha()

i = 0
error = 0
while i < 10 and error < 10:
    try:
        begin = int(round(time.time() * 1000))
        images = requests.post("https://api.jingjia-tech.com/htsec/api/captcha/gen").json()
        captcha_id = images['data']['id']
        image_search_str = images['data']['captcha']['templateImage']
        image_str = images['data']['captcha']['backgroundImage']
        backgroundImageWidth = images['data']['captcha']['backgroundImageWidth']
        backgroundImageHeight = images['data']['captcha']['backgroundImageHeight']
        templateImageWidth = images['data']['captcha']['templateImageWidth']
        templateImageHeight = images['data']['captcha']['templateImageHeight']

        image_search_str = image_search_str[image_search_str.index(',') + 1:]
        image_str = image_str[image_str.index(',') + 1:]
        image_search = base64.b64decode(image_search_str)
        image = base64.b64decode(image_str)
        captcha_result = captcha.search(image_search, image)
        trackList = captcha_result['track_list']

        post_json = {
            "id": captcha_id,
            "data": {
                "bgImageWidth": backgroundImageWidth,
                "bgImageHeight": backgroundImageHeight,
                "sliderImageWidth": templateImageWidth,
                "sliderImageHeight": templateImageHeight,
                "startSlidingTime": begin,
                "endSlidingTime": int(round(time.time() * 1000)),
                "trackList": trackList
            }
        }
        valid_result = requests.post("https://api.jingjia-tech.com/htsec/api/captcha/valid",
                                     data=json.dumps(post_json), headers=headers).json()
        if valid_result['code'] == 0:
            register_json = {
                "username": aes_encrypt(fake.name(), "P+Rq948CrN3oXN76"),
                "phone": aes_encrypt(fake.phone_number(), "P+Rq948CrN3oXN76"),
                "innerSchoolCode": "",
                "captchaToken": captcha_id,
                "schoolCode": "4144014063"
            }
            register_result = requests.post("https://api.jingjia-tech.com/htsec/api/project/questionnaire/register",
                                            data=json.dumps(register_json), headers=headers).json()
            if register_result['code'] == 0:
                print("register success " + captcha_id)
                i += 1
            else:
                print("register error " + captcha_id)
                print(register_result)
                error += 1
            time.sleep(30)
        else:
            with open('./images/' + captcha_id + '.png', 'wb') as file:
                file.write(image_search)
            with open('./images/' + captcha_id + '.jpg', 'wb') as file:
                file.write(image)
            captcha.save_result("./images/" + captcha_id + "result.jpg")
            print("captcha error " + captcha_id)
            print(valid_result)
            error += 1
            time.sleep(3)
    except Exception as e:
        print("unknown error ")
        error += 1
        time.sleep(10)
        continue

