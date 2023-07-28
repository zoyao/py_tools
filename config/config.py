import os
import yaml


class conf(object):
    def __init__(self, base_dir='.'):
        self.base_dir = base_dir
        with open(os.path.expanduser(base_dir + "/resources/config.yaml"), "r", encoding='utf-8') as config:
            self.cfg = yaml.safe_load(config)

    def reload(self):
        with open(os.path.expanduser(self.base_dir + "/resources/config.yaml"), "r", encoding='utf-8') as config:
            self.cfg = yaml.safe_load(config)

    def get_check_list(self):
        return self.cfg['check']['lukou']['list']

    def get_interval(self):
        return self.cfg['check']['lukou']['interval']

    def get_pushdeer_url(self):
        return str(self.cfg['notice']['pushdeer']['url'])

    def get_users(self):
        return self.cfg['users']

    def get_lukou_username(self):
        return str(self.cfg['lukou']['username'])

    def get_lukou_password(self):
        return str(self.cfg['lukou']['password'])
