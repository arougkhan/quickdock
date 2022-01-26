import functools
import json
from flask import Flask
from flask import request

import db_queries as db
from jwt_security import jwt_util as jwt
from jwt_security import authority_helper as auth
from keymap import Keymap

from app import create_app
application = create_app()

userKeyMaps = db.custom_maps
orgKeyMaps = db.base_maps

@application.route('/ping', methods=['GET'])
def ping():
    return "phrase service: pong"

@application.route('/auth/me', methods=['GET'])
@jwt.usermodel_from_jwt
def show_me(usermodel):
    return usermodel.__dict__, 200

@application.route('/auth/permissions', methods=['GET'])
@jwt.usermodel_from_jwt
def show_rights(usermodel):
    return "Permission checks for user {0}\n".format(usermodel.displayname) + \
           "is_me: {0}\n" .format(auth.is_me(usermodel.user_id)) + \
           "is_user: {0}\n ".format(auth.is_User())


# Utility - backend composition of keymaps: Combines a base keymap with a customization keymap. Values
# from customizations overwrite base values (and for duplicates later entries overwrite earlier ones).
# Map names should be supplied as URL parameters, missing values will use 'default' as name.
@application.route('/keymap/composite-map/<keymap_alias>', methods=['GET'])
@application.route('/keymap/composite-map', methods=['GET'], defaults={'keymap_alias': 'default'})
@jwt.parse_jwt_header
def getCompositeKeymaps(payload, keymap_alias):
    trace = request.args.get('trace')
    userMapAlias = request.args.get('user_map', keymap_alias)
    orgMapAlias = request.args.get('base_map', keymap_alias)
    custom = Keymap.from_json(db.get_key_map(payload['user_id'], userMapAlias, userKeyMaps) )
    base = Keymap.from_json(db.get_key_map(payload['org_id'], orgMapAlias, orgKeyMaps) )
    if trace is None:
        return dict([(item["key"], item["value"]) for item in base.keymap + custom.keymap])
    else:
        return {"user_map": {"alias": custom.keymap_alias, "user_id": payload['user_id']},
                "base_map": {"alias": base.keymap_alias, "org_id:": payload['org_id']},
                "combined_keymap": dict([(item["key"], item["value"]) for item in base.keymap + custom.keymap])}


# --=={ INDIVIDUALIZED KEYMAPS }==--


@application.route('/keymap/user-maps', methods=['GET'])
@jwt.user_from_jwt
def getKeymaps(user_id):
    return db.get_key_maps(user_id, userKeyMaps)


@application.route('/keymap/user-map/<keymap_alias>', methods=['GET'])
@jwt.user_from_jwt
def getKeymap(user_id, keymap_alias):
    return db.get_key_map_no_uid(user_id, keymap_alias, userKeyMaps)


@application.route('/keymap/user-map/<keymap_alias>', methods=['DELETE'])
@jwt.user_from_jwt
def deleteKeymap(user_id, keymap_alias):
    return db.delete_key_map(user_id, keymap_alias, userKeyMaps)


@application.route('/keymap/user-map', methods=['POST', 'PUT'], defaults={'keymap_alias': None})
@application.route('/keymap/user-map/<keymap_alias>', methods=['POST', 'PUT'])
@jwt.user_from_jwt
def saveKeymap(user_id, keymap_alias):
    keymap = Keymap.from_json(request.data)
    keymap.user_id = user_id
    if keymap_alias:
        keymap.keymap_alias = keymap_alias
    return db.save_key_map(keymap, userKeyMaps)


@application.route('/keymap/user-map/<keymap_alias>/items/<key_name>', methods=['POST', 'PUT'])
@jwt.user_from_jwt
def addKeymapItemByKeyname(user_id, keymap_alias, key_name):
    mapping = {"key": key_name, "value": request.data.decode()}
    return addKeymapItem(user_id, keymap_alias, mapping)


@application.route('/keymap/user-map/<keymap_alias>/items', methods=['POST', 'PUT'])
@jwt.user_from_jwt
def addKeymapItemByObject(user_id, keymap_alias):
    mapping = json.loads(request.data)
    return addKeymapItem(user_id, keymap_alias, mapping)


# Service method: add or update item in keymap
def addKeymapItem(user_id, keymap_alias, new_item):
    current = Keymap.from_json(db.get_key_map(user_id, keymap_alias, userKeyMaps))
    current.keymap = list({item['key']: item for item in current.keymap + [new_item]}.values())
    return db.save_key_map(current, userKeyMaps)


@application.route('/keymap/user-map/<keymap_alias>/items/<key_name>', methods=['DELETE'])
@jwt.user_from_jwt
def clearKeymapItemByName(user_id, keymap_alias, key_name):
    return clearKeymapItem(user_id, keymap_alias, key_name)


@application.route('/keymap/user-map/<keymap_alias>/items', methods=['DELETE'])
@jwt.user_from_jwt
def clearKeymapItemByObject(user_id, keymap_alias):
    item = json.loads(request.data)
    return clearKeymapItem(user_id, keymap_alias, item['key'])


# Service method: clear item from keymap
def clearKeymapItem(user_id, keymap_alias, item_name):
    current = Keymap.from_json(db.get_key_map(user_id, keymap_alias, userKeyMaps))
    current.keymap = list(filter(lambda item: item['key'] != item_name, current.keymap))
    return db.save_key_map(current, userKeyMaps)


# --=={ BASE/ORGANIZATION KEYMAPS }==--


@application.route('/keymaps/base', methods=['GET'])
@jwt.organization_from_jwt
def getBaseKeyMaps(organization_id):
    return db.get_key_maps(organization_id, orgKeyMaps)


@application.route('/keymap/base-map/<keymap_alias>', methods=['GET'])
@jwt.organization_from_jwt
def getBaseKeyMap(organization_id, keymap_alias):
    return db.get_key_map_no_uid(organization_id, keymap_alias, orgKeyMaps)


@application.route('/keymap/base-map/<keymap_alias>', methods=['DELETE'])
@jwt.organization_from_jwt
def deleteBaseKeyMap(organization_id, keymap_alias):
    return db.delete_key_map(organization_id, keymap_alias, orgKeyMaps)


@application.route('/keymap/base-map', methods=['POST', 'PUT'], defaults={'keymap_alias': None})
@application.route('/keymap/base-map/<keymap_alias>', methods=['POST', 'PUT'])
@jwt.organization_from_jwt
def saveBaseKeyMap(organization_id, keymap_alias):
    keymap = Keymap.from_json(request.data)
    keymap.user_id = organization_id
    if keymap_alias:
        keymap.keymap_alias = keymap_alias
    return db.save_key_map(keymap, orgKeyMaps)


@application.route('/keymap/base-map/<keymap_alias>/items/<key_name>', methods=['POST', 'PUT'])
@jwt.organization_from_jwt
def addBaseKeymapItemByKeyname(org_id, keymap_alias, key_name):
    mapping = {"key": key_name, "value": request.data.decode()}
    return addBaseKeymapItem(org_id, keymap_alias, mapping)


@application.route('/keymap/base-map/<keymap_alias>/items', methods=['POST', 'PUT'])
@jwt.organization_from_jwt
def addBaseKeymapItemByObject(org_id, keymap_alias):
    mapping = json.loads(request.data)
    return addBaseKeymapItem(org_id, keymap_alias, mapping)


# Service method: add or update item in keymap
def addBaseKeymapItem(org_id, keymap_alias, new_item):
    current = Keymap.from_json(db.get_key_map(org_id, keymap_alias, orgKeyMaps))
    current.keymap = list({item['key']: item for item in current.keymap + [new_item]}.values())
    return db.save_key_map(current, orgKeyMaps)


@application.route('/keymap/base-map/<keymap_alias>/items/<key_name>', methods=['DELETE'])
@jwt.organization_from_jwt
def clearBaseKeymapItemByName(org_id, keymap_alias, key_name):
    return clearBaseKeymapItem(org_id, keymap_alias, key_name)


@application.route('/keymap/base-map/<keymap_alias>/items', methods=['DELETE'])
@jwt.organization_from_jwt
def clearBaseKeymapItemByObject(org_id, keymap_alias):
    item = json.loads(request.data)
    return clearBaseKeymapItem(org_id, keymap_alias, item['key'])


# Service method: clear item from keymap
def clearBaseKeymapItem(org_id, keymap_alias, item_name):
    current = Keymap.from_json(db.get_key_map(org_id, keymap_alias, orgKeyMaps))
    current.keymap = list(filter(lambda item: item['key'] != item_name, current.keymap))
    return db.save_key_map(current, orgKeyMaps)

# Run as standalone app
if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')






