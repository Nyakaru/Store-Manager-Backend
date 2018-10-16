"""App configuration."""

import os


class Config(object):
    """Base config class."""

    SECRET_KEY = os.environ['APP_SECRET_KEY']


class TestingConfig(Config):
    """Config for testing environment."""

    DEBUG = True


class DevelopmentConfig(Config):
    """Config for development environment."""

    DEBUG = False


configurations = {
    "testing": TestingConfig,
    "development": DevelopmentConfig
}
