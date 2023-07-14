import logging
import time
from check_tool.lukou import lukou
from config.config import conf
from notice_tool import pushdeer
from threading import Thread


def run_interval(base_dir='..'):
    config = conf(base_dir)
    lukou_check = lukou()
    for i in range(10):
        Thread(target=pushdeer.send_notice).start()
    while True:
        try:
            config.reload()
            lukou_check.check(config)
            time.sleep(config.get_interval())
        except Exception as e:
            logging.error(e)


