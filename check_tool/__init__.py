import time
from check_tool.lukou import lukou
from config.config import conf


def run_interval(base_dir='..'):
    config = conf(base_dir)
    lukou_check = lukou()
    while True:
        config.reload()
        lukou_check.check(config)
        time.sleep(config.get_interval())

