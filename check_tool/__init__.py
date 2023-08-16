import logging
import time
from check_tool.lukou import lukou
from config.config import conf
from notice_tool import pushdeer
from threading import Thread
from check_tool import check


def run_interval(base_dir='..'):
    version = 'v1.0.1'
    config = conf(base_dir)
    lukou_check = lukou(config)
    pushdeer.set_config(config)
    for i in range(2):
        Thread(target=pushdeer.send_notice).start()
    check.set_config(config)
    for i in range(5):
        Thread(target=check.check_all).start()
    pushdeer.add_notice_all('版本' + version + '启动成功,消息推送功能正常')
    while True:
        try:
            config.reload()
            lukou_check.check()
            time.sleep(config.get_interval())
        except Exception as e:
            logging.error(e)


