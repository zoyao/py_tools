import logging
import requests
from config.config import conf
import time
import random
from collections import deque


list = deque()
config = conf()


def set_config(con):
    global config
    config = con


def add_notice(user, title, message=''):
    url = config.get_pushdeer_url()
    users = config.get_users()
    list.append(url + 'pushkey=' + users[user]['key'] + '&text=' + title + '&desp=' + message)


def send_notice():
    while True:
        if list:
            message = None
            try:
                message = list.popleft()
            except Exception as e:
                pass
            if message:
                try:
                    requests.get(message)
                except Exception as e:
                    list.appendleft(message)
                    logging.error(e)
                continue
        time.sleep(random.uniform(1, 2))
        continue

