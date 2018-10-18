"""
Need method to create config if doesn't exist

Most of this ripped out from the Databricks CLI, need to acknowledge in README
"""
from configparser import ConfigParser
import os
from os.path import expanduser, join

HOST = 'host'
USERNAME = 'username'
PASSWORD = 'password'
TOKEN = 'token'
INSECURE = 'insecure'
DEFAULT_SECTION = 'DEFAULT'

def _get_path():
    _home = expanduser('~')
    return join(_home, '.databrickscfg')

def _fetch_from_fs():
    raw_config = ConfigParser()
    raw_config.read(_get_path())
    return raw_config

def _get_option_if_exists(raw_config, profile, option):
    if profile == DEFAULT_SECTION:
        return raw_config.get(profile, option) if raw_config.has_option(profile, option) else None
    elif option not in raw_config._sections.get(profile, {}).keys():
        return None
    return raw_config.get(profile, option)

def get_config(profile=DEFAULT_SECTION):
    raw_config = _fetch_from_fs()
    host = _get_option_if_exists(raw_config, profile, HOST)
    username = _get_option_if_exists(raw_config, profile, USERNAME)
    password = _get_option_if_exists(raw_config, profile, PASSWORD)
    token = _get_option_if_exists(raw_config, profile, TOKEN)
    insecure = _get_option_if_exists(raw_config, profile, INSECURE)
    config = DatabricksConfig(host, username, password, token, insecure)
    if config.is_valid:
        return config
    return None


class DatabricksConfig(object):
    def __init__(self, host, username, password, token, insecure):
        self.host = host
        self.username = username
        self.password = password
        self.token = token
        self.insecure = insecure

    @classmethod
    def from_token(cls, host, token, insecure=None):
        return DatabricksConfig(host, None, None, token, insecure)

    @classmethod
    def from_password(cls, host, username, password, insecure=None):
        return DatabricksConfig(host, username, password, None, insecure)

    @classmethod
    def empty(cls):
        return DatabricksConfig(None, None, None, None, None)

    @property
    def is_valid_with_token(self):
        return self.host is not None and self.token is not None

    @property
    def is_valid_with_password(self):
        return self.host is not None and self.username is not None and self.password is not None

    @property
    def is_valid(self):
        return self.is_valid_with_token or self.is_valid_with_password
