import logging
import re
from collections import deque
import time
import random
from notice_tool import pushdeer
from config.config import conf


list = deque()
config = conf()


def set_config(con):
    global config
    config = con


def add_check(id, detail):
    message = {
        "id": id,
        "detail": detail
    }
    list.append(message)


def check_all():
    while True:
        if list:
            message = None
            try:
                message = list.popleft()
            except Exception as e:
                pass
            if message:
                try:
                    # 检查是否有匹配内容
                    for c in config.get_check_list():
                        user = c['user']
                        flag, words = check(c, message['detail'])
                        if flag:
                            # 调用通知接口
                            share_url = 'https://www.lukou.cn/sharefeed/' + message['id']
                            pushdeer.add_notice(user, '路口' + words,
                                                url_format(message['detail']) + '  <' + share_url + '>  ')
                except Exception as e:
                    list.appendleft(message)
                    logging.error(e)
                continue
        time.sleep(random.uniform(1, 2))
        continue


def check(c, detail):
    flag = False
    words = '【无】'
    if 'keywords' in c.keys():
        words = ''
        for keys_default in c['keywords']:
            keys = str(keys_default)
            # keywords 内任意满足即可
            key_flag = True
            for key in keys.split(','):
                # 以','分割内容需全部满足
                if key not in detail:
                    # 匹配失败
                    key_flag = False
                    break
            if key_flag:
                # 匹配成功
                flag = True
                words += '【' + keys + '】'
    else:
        # keywords 无数据，全部推送
        flag = True
    return flag, words


def url_format(text):
    # findall() 查找匹配正则表达式的字符串
    chs = re.findall('[\u4e00-\u9fa5]', text)
    text_no_chs = text
    for ch in chs:
        text_no_chs = text_no_chs.replace(ch, ' ')
    urls = re.findall('(http|https)(://[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4})(/[a-zA-Z0-9./_-]+)(\\?[a-zA-Z0-9=&]+)?(#\\S+)?', text_no_chs)
    for url_list in urls:
        url = ''
        for ur in url_list:
            url += ur
        text = text.replace(url, '  <' + url + '>  ')
    return text.replace('&', '%26')
