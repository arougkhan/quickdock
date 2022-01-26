import os

env = os.environ

# Use os.environ["KEY_NAME"] instead of os.environ.get("KEY_NAME")
# to raise exception if no matching key is found.

# Configuration for jwks_util module.
jwks_config = {
    "host": env.get("IDP_JWKS_HOST"),
    "port": env.get("IDP_JWKS_PORT", 8080),
    "path": env.get("IDP_JWKS_PATH"),
    "jwks_url": env.get("IDP_JWKS_HOST") + ":" + env.get("IDP_JWKS_PORT") + env.get("IDP_JWKS_PATH"),
    "audience": env.get("IDP_JWT_AUDIENCE")
}
# Configuration for jwt_util module.
jwt_config = {
    "validation_disabled": (os.environ.get('DISABLE_JWT_VALIDATION', 'false') == 'true'),
    "jwt_bypass_enabled": (os.environ.get('ENFORCE_JWT_AUTHENTICATION', 'false') == 'false'),
}