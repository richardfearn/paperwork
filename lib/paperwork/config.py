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
            home_dir = os.path.expanduser("~")
            filename = os.path.join(home_dir, DEFAULT_CONFIG_FILE)

        self.filename = filename

        self.config = configparser.RawConfigParser()
        self.config.read(self.filename)

    def consumer_key(self):
        """Returns the consumer key."""
        return self.config.get(PAPERWORK_SECTION, "consumer_key")

    def consumer_secret(self):
        """Returns the consumer secret."""
        return self.config.get(PAPERWORK_SECTION, "consumer_secret")

    def has_credentials(self, username):
        """Returns true if this configuration contains credentials for the
        specified user."""
        return self.config.has_section(username)

    def add_credentials(self, username, token, token_secret):
        """Adds credentials for the specified user."""
        self.config.add_section(username)
        self.config.set(username, "token", token)
        self.config.set(username, "token_secret", token_secret)
        self.save()

    def remove_credentials(self, username):
        """Removes credentials for the specified user."""
        self.config.remove_section(username)
        self.save()

    def save(self):
        """Saves this configuration."""
        with open(self.filename, "w") as configfile:
            self.config.write(configfile)

    def token(self, username):
        """Returns the token for the specified username."""
        return self.config.get(username, "token")

    def token_secret(self, username):
        """Returns the token secret for the specified username."""
        return self.config.get(username, "token_secret")
