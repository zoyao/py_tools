import requests
import os
import yaml

# https://api2.pushdeer.com/message/push?pushkey=PDU21883Tv6bAqX9srtXSmEKKYBY7arK3QilSMLap&text=%E8%A6%81%E5%8F%91%E9%80%81%E7%9A%84%E5%86%85%E5%AE%B9
url = ''
users = {}

with open(os.path.expanduser("../config/config.yaml"), "r", encoding='utf-8') as config:
    cfg = yaml.safe_load(config)
    url = cfg['notice']['url']
    users = cfg['users']


def send_notice(user, title, message=''):
    requests.get(url + 'pushkey=' + users[user]['key'] + '&text=' + title + '&desp=' + message)
