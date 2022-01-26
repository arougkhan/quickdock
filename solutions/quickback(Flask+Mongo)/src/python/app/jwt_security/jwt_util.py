import functools
import jwt
from flask import request

from jwt_security.config import jwt_config as config
from jwt_security.classes import Usermodel
import jwt_security.jwks_util as jwks

################################################################
# JWT utility for WDX and the Flask framework                  #
#                                                              #
# Use as decorators to wrap calling function. Functions assume #
# assume a valid Flask HTTP request is present in the context  #
# when called.                                                 #
################################################################

# Check for, extract and decode JWT content in Authorization header.
def parse_jwt_header(f):
    @functools.wraps(f)
    def with_parsed_payload(*args, **kwargs):
        jwt_token = request.headers.get('Authorization', None)
        if jwt_token:
            if jwt_token.startswith("Bearer "):
                jwt_token = jwt_token[len("Bearer "):]
            try:
                if config["validation_disabled"]:
                    jwt_payload = jwt.decode(jwt_token, options={"verify_signature": False})
                else:
                    jwt_payload = jwks.decode(jwt_token)
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return 'JWT token is expired', 400
        else:
            # Allow fallback to query parameters if 'jwt_auth_disabled' is set.
            if config["jwt_bypass_enabled"]:
                jwt_payload = {'user_id':request.args.get('userId', 'default'),
                               'group_id':request.args.get('groupId', 'default'),
                               'org_id':request.args.get('orgId', 'default'),}
                return f(jwt_payload, *args, **kwargs)
            else:
                return "JWT authorization token not found", 400
        return f(jwt_payload, *args, **kwargs)
    return with_parsed_payload


# Verify that user_id parameter matches 'user_id' in JWT
def matches_user(f):
    @functools.wraps(f)
    def matches_user_wrapper(jwt_payload, user_id, *args, **kwargs):
        if jwt_payload["user_id"] == user_id:
            return f(user_id, *args, **kwargs)
        else:
            return 'Supplied user_id does not match claim in JWT', 400
    return parse_jwt_header(matches_user_wrapper)

# Extract user_id from JWT
def user_from_jwt(f):
    @functools.wraps(f)
    def user_from_jwt_wrapper(jwt_payload, *args, **kwargs):
        if jwt_payload["user_id"]:
            return f(jwt_payload["user_id"], *args, **kwargs)
        else:
            return 'No user_id claim found in JWT', 400
    return parse_jwt_header(user_from_jwt_wrapper)


# Verify that org_id parameter matches 'org_id' in JWT
def matches_organization(f):
    @functools.wraps(f)
    def matches_organization_wrapper(jwt_payload, organization_id, *args, **kwargs):
        if jwt_payload["org_id"] == organization_id:
            return f(organization_id, *args, **kwargs)
        else:
            return 'Supplied org_id does not match claim in JWT', 400
    return parse_jwt_header(matches_organization_wrapper)

# Extract org_id from JWT
def organization_from_jwt(f):
    @functools.wraps(f)
    def organization_from_jwt_wrapper(jwt_payload, *args, **kwargs):
        if jwt_payload["org_id"]:
            return f(jwt_payload["org_id"], *args, **kwargs)
        else:
            return 'No org_id claim found in JWT, 400'
    return parse_jwt_header(organization_from_jwt_wrapper)

# Extract user_id and org_id from JWT
def user_and_org_from_jwt(f):
    @functools.wraps(f)
    def user_and_org_from_jwt_wrapper(jwt_payload, *args, **kwargs):
        if jwt_payload["user_id"]:
            if jwt_payload["org_id"]:
                return f(jwt_payload["user_id"], jwt_payload["org_id"], *args, **kwargs)
            else:
                return 'No org_id claim found in JWT', 400
        else:
            return 'No user_id claim found in JWT', 400
    return parse_jwt_header(user_and_org_from_jwt_wrapper)

# Extract Usermodel from JWT
def usermodel_from_jwt(f):
    @functools.wraps(f)
    def  add_usermodel_wrapper(jwt_payload, *args, **kwargs):
        return f(Usermodel.load_from_jwt(jwt_payload), *args, **kwargs)
    return parse_jwt_header(add_usermodel_wrapper)



