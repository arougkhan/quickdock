from config import jwks_config as config
import requests
import json
import jwt

# Allowed algorithms:
allowed_algorithms = ['RS256']
intended_audience = config['audience']
public_keys = {}


def load_jwks():
    try:
        response = requests.get(config["jwks_url"])
        jwks = json.loads(response.content)
        for jwk in jwks['keys']:
            kid = jwk['kid']
            public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
    except ConnectionRefusedError:
        return "Connection refused"


def get_key(kid):
    if kid not in public_keys:
        load_jwks()
    return public_keys[kid]


def decode(jwt_token):
    kid = jwt.get_unverified_header(jwt_token)['kid']
    return jwt.decode(jwt_token, get_key(kid), audience=intended_audience, algorithms=allowed_algorithms)
