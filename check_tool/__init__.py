from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from lukou2 import lukou
import os
import yaml


class my_CronTrigger(CronTrigger):
    @classmethod
    def my_from_crontab(cls, expr, timezone=None):
        values = expr.split()
        if len(values) != 7:
            raise ValueError('Wrong number of fields; got {}, expected 7'.format(len(values)))

        return cls(second=values[0], minute=values[1], hour=values[2], day=values[3], month=values[4],
                   day_of_week=values[5], year=values[6], timezone=timezone)


with open(os.path.expanduser("../config/config.yaml"), "r", encoding='utf-8') as config:
    cfg = yaml.safe_load(config)
    check_lukou_cron = cfg['check']['lukou']['cron']
lukou_check = lukou()
schedule = BlockingScheduler()
schedule.add_job(lukou_check.check, my_CronTrigger.my_from_crontab(check_lukou_cron))
schedule.start()