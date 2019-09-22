"""
paperwork config module

This module includes the Config class, which can be used to read paperwork
configuration files.
"""

import configparser

import os

DEFAULT_CONFIG_FILE = ".paperworkrc"

PAPERWORK_SECTION = "paperwork"


class Config:

    """Holds configuration used when making requests to Instapaper."""

    def __init__(self, filename=None):

        if filename is None:
            filename = os.path.join(os.path.expanduser("~"), DEFAULT_CONFIG_FILE)

        self.filename = filename

        self.config = configparser.RawConfigParser()
        self.config.read(self.filename)

    def consumer_key(self):
        """Returns the consumer key."""
        return self.config.get(PAPERWORK_SECTION, "consumer_key")

    def consumer_secret(self):
        """Returns the consumer secret."""
        return self.config.get(PAPERWORK_SECTION, "consumer_secret")

    def token(self, username):
        """Returns the token for the specified username."""
        return self.config.get(username, "token")

    def token_secret(self, username):
        """Returns the token secret for the specified username."""
        return self.config.get(username, "token_secret")
