import configparser

import os

DEFAULT_CONFIG_FILE = ".paperworkrc"

PAPERWORK_SECTION = "paperwork"


class Config:

    def __init__(self, filename=None):

        if filename is None:
            filename = os.path.join(os.path.expanduser("~"), DEFAULT_CONFIG_FILE)

        self.filename = filename

        self.config = configparser.RawConfigParser()
        self.config.read(self.filename)

    def consumer_key(self):
        return self.config.get(PAPERWORK_SECTION, "consumer_key")

    def consumer_secret(self):
        return self.config.get(PAPERWORK_SECTION, "consumer_secret")

    def token(self, username):
        return self.config.get(username, "token")

    def token_secret(self, username):
        return self.config.get(username, "token_secret")
