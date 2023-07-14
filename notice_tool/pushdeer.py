import requests
from config.config import conf


def send_notice(user, title, message='', config=conf()):
    url = config.get_pushdeer_url()
    users = config.get_users()
    requests.get(url + 'pushkey=' + users[user]['key'] + '&text=' + title + '&desp=' + message)