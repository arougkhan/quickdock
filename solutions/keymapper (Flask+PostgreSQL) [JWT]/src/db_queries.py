import sys

#from bson.json_util import dumps
from config import postgres_config as config
import psycopg2
import json
from pprint import pprint

conn = psycopg2.connect(config['connection_string'])

## Define database tables
custom_maps = "custom_maps"
base_maps = "base_maps"

# SQL
GET_KEYMAP = "SELECT keymap FROM {collection} WHERE user_id = '{uid}' and keymap_alias = '{alias}';"
GET_KEYMAP_AND_ID = "SELECT keymap, id FROM {collection} WHERE user_id = '{uid}' and keymap_alias = '{alias}';"
GET_KEYMAPS = "SELECT keymap_alias FROM {collection} WHERE user_id = '{uid}';"
DELETE_KEYMAP = "DELETE FROM {collection} WHERE user_id = '{uid}' and keymap_alias = '{alias}';"
INSERT_OR_UPDATE_KEYMAP = "INSERT INTO {collection} (user_id, keymap_alias, keymap) VALUES('{uid}', '{alias}', '{keymap}') " \
                          + "ON CONFLICT(user_id, keymap_alias) DO UPDATE SET keymap = '{keymap}';"


def run_query(query_name, args, select_operation=True):
    try:
        with conn.cursor() as cursor:
            cursor.execute(query_name.format(**args))
            return cursor.fetchall() if select_operation else cursor.statusmessage
    except Exception as e:
        raise Exception("DB Query to postgres failed: {0}".format(str(e)))


def get_key_map_no_uid(user_id, keymap_alias, collection):
    result = run_query(GET_KEYMAP, {'collection': collection, 'uid': user_id, 'alias': keymap_alias})
    return '{"keymap_alias": "%s", "keymap": %s}' % (keymap_alias, json.dumps(result[0][0]))  # Unpack list of tuples


def get_key_map(user_id, keymap_alias, collection):
    result = run_query(GET_KEYMAP_AND_ID, {'collection': collection, 'uid': user_id, 'alias': keymap_alias})
    return '{"user_id": "%s", "keymap_alias": "%s", "keymap": %s}' % (user_id, keymap_alias, json.dumps(result[0][0]))


def get_key_maps(user_id, collection):
    result = run_query(GET_KEYMAPS, {'collection': collection, 'uid': user_id})
    return json.dumps([{'keymap_alias': r[0]} for r in result])


def save_key_map(keymap, collection):
    result = run_query(INSERT_OR_UPDATE_KEYMAP, {'collection': collection, 'uid': keymap.user_id, 'alias': keymap.keymap_alias, 'keymap': json.dumps(keymap.keymap)}, False)
    return result


def delete_key_map(user_id, keymap_alias, collection):
    result = run_query(DELETE_KEYMAP,  {'collection': collection, 'uid': user_id, 'alias': keymap_alias}, False)
    return result




