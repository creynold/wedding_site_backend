import configparser

class Config(object):

    def __init__(self):
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.read('wedding_site_backend/config.ini')

    def get(self, group, key):
        return self.config[group][key]

    def get_group(self, group):
        return self.config[group]
