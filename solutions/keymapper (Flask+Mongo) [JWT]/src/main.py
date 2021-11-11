import functools
import locale
import os
import sys
from pprint import pprint

import jwt
from flask import Flask
from flask import request
from flask_cors import CORS

import json
import db_queries as db
import jwks
from config import controller_config as config
from keymap import Keymap

app = Flask(__name__)
CORS(app)

userKeyMaps = db.custom_maps
orgKeyMaps = db.base_maps

# Check for and extract content from JWT in Authorization header
def jwt_checker(f):
    @functools.wraps(f)
    def jwt_wrapper(*args, **kwargs):
        jwt_token = request.headers.get('Authorization', None)
        if jwt_token:
            if jwt_token.startswith("Bearer "):
                jwt_token = jwt_token[len("Bearer "):]
            try:
                if config["validation_disabled"]:
                    payload = jwt.decode(jwt_token, options={"verify_signature": False})
                else:
                   payload = jwks.decode(jwt_token)
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return 'JWT token is expired', 400
        else:
            return "JWT authorization token not found", 400
        return f(payload, *args, **kwargs)
    return jwt_wrapper


# Verify that user_id in JWT payload and function call match
# Uses jwt_checker decorator to extract JWT token
def user_checker(f):
    @functools.wraps(f)
    def user_check_wrapper(jwt_payload, user_id, *args, **kwargs):
        if jwt_payload["user_id"] == user_id:
            return f(user_id, *args, **kwargs)
        else:
            return 'JWT user does not match user in invocation  path', 400
    return jwt_checker(user_check_wrapper)


def user_from_jwt(f):
    @functools.wraps(f)
    def user_from_jwt_wrapper(jwt_payload, *args, **kwargs):
        if jwt_payload["user_id"]:
            return f(jwt_payload["user_id"], *args, **kwargs)
        else:
            return 'No user_id claim found in JWT', 400
    return jwt_checker(user_from_jwt_wrapper)


# Verify that org_id in JWT payload and function call match
# Uses jwt_checker decorator to extract JWT token
def organization_checker(f):
    @functools.wraps(f)
    def organization_check_wrapper(jwt_payload, organization_id, *args, **kwargs):
        if jwt_payload["org_id"] == organization_id:
            return f(organization_id, *args, **kwargs)
        else:
            return 'JWT user does not match user in invocation  path', 400
    return jwt_checker(organization_check_wrapper)


def organization_from_jwt(f):
    @functools.wraps(f)
    def organization_from_jwt_wrapper(jwt_payload, *args, **kwargs):
        if jwt_payload["org_id"]:
            return f(jwt_payload["org_id"], *args, **kwargs)
        else:
            return 'No org_id claim found in JWT, 400'
    return jwt_checker(organization_from_jwt_wrapper)


@app.route('/ping', methods=['GET'])
def ping():
    return "mongo pong"


# Utility - backend composition of keymaps: Combines a base keymap with a customization keymap. Values
# from customizations overwrite base values (and for duplicates later entries overwrite earlier ones).
# Map names should be supplied as URL parameters, missing values will use 'default' as name.
@app.route('/composite/keymap', methods=['GET'])
@jwt_checker
def getCompositeKeymaps(payload):
    trace = request.args.get('trace')
    userMapAlias = request.args.get('user_map', 'default')
    orgMapAlias = request.args.get('base_map', 'default')
    custom = Keymap.from_json(db.get_key_map(payload['user_id'], userMapAlias, userKeyMaps) )
    base = Keymap.from_json(db.get_key_map(payload['org_id'], orgMapAlias, orgKeyMaps) )
    if trace is None:
        return dict([(item["key"], item["value"]) for item in base.keymap + custom.keymap])
    else:
        return {"user_map": {"alias": custom.keymap_alias, "user_id": payload['user_id']},
                "base_map": {"alias": base.keymap_alias, "org_id:": payload['org_id']},
                "combined_keymap": dict([(item["key"], item["value"]) for item in base.keymap + custom.keymap])}


# --=={ INDIVIDUALIZED KEYMAPS }==--


@app.route('/user/keymaps', methods=['GET'])
@user_from_jwt
def getKeymaps(user_id):
    return db.get_key_maps(user_id, userKeyMaps)


@app.route('/user/keymap/<keymap_alias>', methods=['GET'])
@user_from_jwt
def getKeymap(user_id, keymap_alias):
    return db.get_key_map_no_uid(user_id, keymap_alias, userKeyMaps)


@app.route('/user/keymap/<keymap_alias>', methods=['DELETE'])
@user_from_jwt
def deleteKeymap(user_id, keymap_alias):
    return db.delete_key_map(user_id, keymap_alias, userKeyMaps)


@app.route('/user/keymap', methods=['POST', 'PUT'], defaults={'keymap_alias': None})
@app.route('/user/keymap/<keymap_alias>', methods=['POST', 'PUT'])
@user_from_jwt
def saveKeymap(user_id, keymap_alias):
    keymap = Keymap.from_json(request.data)
    keymap.user_id = user_id
    if keymap_alias:
        keymap.keymap_alias = keymap_alias
    return db.save_key_map(keymap, userKeyMaps)


@app.route('/user/keymap/<keymap_alias>/items/<key_name>', methods=['POST', 'PUT'])
@user_from_jwt
def addKeymapItemByKeyname(user_id, keymap_alias, key_name):
    mapping = {"key": key_name, "value": request.data.decode()}
    return addKeymapItem(user_id, keymap_alias, mapping)


@app.route('/user/keymap/<keymap_alias>/items', methods=['POST', 'PUT'])
@user_from_jwt
def addKeymapItemByObject(user_id, keymap_alias):
    mapping = json.loads(request.data)
    return addKeymapItem(user_id, keymap_alias, mapping)


# Service method: add or update item in keymap
def addKeymapItem(user_id, keymap_alias, new_item):
    current = Keymap.from_json(db.get_key_map(user_id, keymap_alias, userKeyMaps))
    current.keymap = list({item['key']: item for item in current.keymap + [new_item]}.values())
    return db.save_key_map(current, userKeyMaps)


@app.route('/user/keymap/<keymap_alias>/items/<key_name>', methods=['DELETE'])
@user_from_jwt
def clearKeymapItemByName(user_id, keymap_alias, key_name):
    return clearKeymapItem(user_id, keymap_alias, key_name)


@app.route('/user/keymap/<keymap_alias>/items', methods=['DELETE'])
@user_from_jwt
def clearKeymapItemByObject(user_id, keymap_alias):
    item = json.loads(request.data)
    return clearKeymapItem(user_id, keymap_alias, item['key'])


# Service method: clear item from keymap
def clearKeymapItem(user_id, keymap_alias, item_name):
    current = Keymap.from_json(db.get_key_map(user_id, keymap_alias, userKeyMaps))
    current.keymap = list(filter(lambda item: item['key'] != item_name, current.keymap))
    return db.save_key_map(current, userKeyMaps)


# --=={ BASE/ORGANIZATION KEYMAPS }==--


@app.route('/base/keymaps', methods=['GET'])
@organization_from_jwt
def getBaseKeyMaps(organization_id):
    return db.get_key_maps(organization_id, orgKeyMaps)


@app.route('/base/keymap/<keymap_alias>', methods=['GET'])
@organization_from_jwt
def getBaseKeyMap(organization_id, keymap_alias):
    sys.stderr.write(locale.getpreferredencoding())
    sys.stderr.write(sys.getfilesystemencoding())
    sys.stderr.write(">>>>>>>>>" + keymap_alias)
    return db.get_key_map_no_uid(organization_id, keymap_alias, orgKeyMaps)


@app.route('/base/keymap/<keymap_alias>', methods=['DELETE'])
@organization_from_jwt
def deleteBaseKeyMap(organization_id, keymap_alias):
    return db.delete_key_map(organization_id, keymap_alias, orgKeyMaps)


@app.route('/base/keymap', methods=['POST', 'PUT'], defaults={'keymap_alias': None})
@app.route('/base/keymap/<keymap_alias>', methods=['POST', 'PUT'])
@organization_from_jwt
def saveBaseKeyMap(organization_id, keymap_alias):
    keymap = Keymap.from_json(request.data)
    keymap.user_id = organization_id
    if keymap_alias:
        keymap.keymap_alias = keymap_alias
    return db.save_key_map(keymap, orgKeyMaps)


@app.route('/base/keymap/<keymap_alias>/items/<key_name>', methods=['POST', 'PUT'])
@organization_from_jwt
def addBaseKeymapItemByKeyname(org_id, keymap_alias, key_name):
    mapping = {"key": key_name, "value": request.data.decode()}
    return addBaseKeymapItem(org_id, keymap_alias, mapping)


@app.route('/base/keymap/<keymap_alias>/items', methods=['POST', 'PUT'])
@organization_from_jwt
def addBaseKeymapItemByObject(org_id, keymap_alias):
    mapping = json.loads(request.data)
    return addBaseKeymapItem(org_id, keymap_alias, mapping)


# Service method: add or update item in keymap
def addBaseKeymapItem(org_id, keymap_alias, new_item):
    current = Keymap.from_json(db.get_key_map(org_id, keymap_alias, orgKeyMaps))
    current.keymap = list({item['key']: item for item in current.keymap + [new_item]}.values())
    return db.save_key_map(current, orgKeyMaps)


@app.route('/base/keymap/<keymap_alias>/items/<key_name>', methods=['DELETE'])
@organization_from_jwt
def clearBaseKeymapItemByName(org_id, keymap_alias, key_name):
    return clearBaseKeymapItem(org_id, keymap_alias, key_name)


@app.route('/base/keymap/<keymap_alias>/items', methods=['DELETE'])
@organization_from_jwt
def clearBaseKeymapItemByObject(org_id, keymap_alias):
    item = json.loads(request.data)
    return clearBaseKeymapItem(org_id, keymap_alias, item['key'])


# Service method: clear item from keymap
def clearBaseKeymapItem(org_id, keymap_alias, item_name):
    current = Keymap.from_json(db.get_key_map(org_id, keymap_alias, orgKeyMaps))
    current.keymap = list(filter(lambda item: item['key'] != item_name, current.keymap))
    return db.save_key_map(current, orgKeyMaps)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')





