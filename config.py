"""Application configuration."""

import os


class Config(object):
    """Base config class."""

    SECRET_KEY = os.environ.get('APP_SECRET_KEY')


class TestingConfig(Config):
    """Configuration for testing environment."""

    DEBUG = True


class DevelopmentConfig(Config):
    """Configuration for development environment."""

    DEBUG = False
    DATABASE_URL = os.getenv("DATABASE_URL")


configurations = {
    "testing": TestingConfig,
    "development": DevelopmentConfig
}
