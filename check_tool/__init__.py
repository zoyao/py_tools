import time
from check_tool.lukou import lukou
from config.config import conf


def run_interval(base_dir='..'):
    config = conf(base_dir)
    lukou_check = lukou(config)
    while True:
        lukou_check.check()
        config.reload()
        time.sleep(config.get_interval())

