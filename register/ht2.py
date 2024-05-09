import base64
import requests
import json
import time
import random
from faker import Faker
from Crypto.Cipher import AES
from captcha import Captcha
from requests_html import HTMLSession

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
page = "https://www.shtjtv.com/web/#/pages/public/webH5?href=%22https%3A%2F%2Fwork.jingjia-tech.com%2Fhtsec%2Fqs%2F%23%2F1770648471997648896%22"
# page = "https://work.jingjia-tech.com/htsec/qs/#/1770648471997648896?step=5"

session = HTMLSession()

response = session.get(url=page, headers=headers)
response.html.render(keep_page=True, scrolldown=3)
print(response.html.html)
# a = response.html.find('#app')
# pass
# async def run():
#     a = response.html.find('.register-btn')
#
#     # 交互语句
#     await response.html.page.keyboard.press('A')
#
#
#     pass
#
#
# try:
#     session.loop.run_until_complete(run())
# finally:
#     session.close()
