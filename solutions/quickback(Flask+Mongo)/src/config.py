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

jwks_config = {
    "host": env.get("IDP_JWKS_HOST"),
    "port": env.get("IDP_JWKS_PORT"),
    "path": env.get("IDP_JWKS_PATH"),
    "jwks_url": env.get("IDP_JWKS_HOST") + ":" + env.get("IDP_JWKS_PORT") + env.get("IDP_JWKS_PATH"),
    "audience": env.get("IDP_JWT_AUDIENCE")
}

controller_config = {
    "validation_disabled": (os.environ.get('KEYMAP_DISABLE_JWT_VALIDATION', 'false') == 'true')}
