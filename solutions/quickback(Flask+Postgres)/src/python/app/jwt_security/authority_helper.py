import functools

from flask import request
from jwt_security.classes import Usermodel
from jwt_security.jwt_util import usermodel_from_jwt

#################################################
# Role base Authorization with JWT for Flask    #
#                                               #
# Check permissions against JWT claims. Assumes #
# a Flask Http request with an 'Authorization'  #
# header containing the JWT to be validated     #
# against is present in calling context.        #                                      #
#################################################

def is_me(user_id):
    return _matches_user_id(user_id)

def has_role(role):
    return _matches_role(role)

def has_all_roles(roles):
    return _matches_all_roles(roles)

def has_one_or_more_roles(roles):
    return _matches_one_or_more_roles(roles)

@usermodel_from_jwt
def _matches_user_id(usermodel: Usermodel, user_id):
    return usermodel.user_id == user_id

@usermodel_from_jwt
def _matches_role(usermodel: Usermodel, role):
    return role in usermodel.authorities

@usermodel_from_jwt
def _matches_all_roles(usermodel: Usermodel, roles):
    for role in roles:
        if role not in usermodel.authorities:
            return False
    return True

@usermodel_from_jwt
def _matches_one_or_more_roles(usermodel: Usermodel, roles):
    for role in roles:
        if role in usermodel.authorities:
            return True
    return False






