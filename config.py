"""The configuration for the app"""
import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    SECRET_KEY = os.getenv('APP_SECRET_KEY')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing"""
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
