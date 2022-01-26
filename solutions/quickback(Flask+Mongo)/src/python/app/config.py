import os

env = os.environ

# Read docker secrets into environment if present
if env.get("KEYMAP_DB_USERNAME_FILE") is not None:
    os.environ["KEYMAP_DB_USERNAME"] = open(env.get("KEYMAP_DB_USERNAME_FILE")).readline()
if env.get("KEYMAP_DB_PASSWORD_FILE") is not None:
    os.environ["KEYMAP_DB_PASSWORD"] = open(env.get("KEYMAP_DB_PASSWORD_FILE")).readline()

# Use os.environ["KEY_NAME"] instead of os.environ.get("KEY_NAME")
# to raise exception if no matching key is found.
mongo_config = {
    "host": env.get("KEYMAP_DB_HOST"),
    "port": env.get("KEYMAP_DB_PORT"),
    "user": env.get("KEYMAP_DB_USERNAME"),
    "password": env.get("KEYMAP_DB_PASSWORD"),
    "db_name": env.get("KEYMAP_DB_NAME"),
    "db_connection": "mongodb://" + env.get("KEYMAP_DB_USERNAME") +
                     ":" + env.get("KEYMAP_DB_PASSWORD") +
                     "@" + env.get("KEYMAP_DB_HOST") +
                     ":" + env.get("KEYMAP_DB_PORT")
}


class Config:
    """
    Base configuration class. Contains default configuration settings + configuration settings applicable to all environments.
    """
    # Default settings
    FLASK_ENV = 'development'
    WTF_CSRF_ENABLED = False
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    FLASK_ENV = 'production'