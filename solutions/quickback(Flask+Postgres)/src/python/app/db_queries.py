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
GET_KEYMAP = "SELECT keymap FROM {collection} WHERE user_id = %s and keymap_alias = %s;"
GET_KEYMAP_AND_ID = "SELECT keymap, id FROM {collection} WHERE user_id = %s and keymap_alias = %s;"
GET_KEYMAPS = "SELECT keymap_alias FROM {collection} WHERE user_id = %s;"
DELETE_KEYMAP = "DELETE FROM {collection} WHERE user_id = %s and keymap_alias = %s;"
INSERT_OR_UPDATE_KEYMAP = "INSERT INTO {collection} (user_id, keymap_alias, keymap) VALUES(%s, %s, %s) " \
                          + "ON CONFLICT(user_id, keymap_alias) DO UPDATE SET keymap = %s;"


def run_query(query_name, args, select_operation=True):
    with psycopg2.connect(config['connection_string']) as conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(query_name,args)
                return cursor.fetchall() if select_operation else cursor.statusmessage
        except Exception as e:
            # How to handle db failures robustly? This renews connection on each failure but might itself fail.
            raise Exception("DB Query to postgres failed: {0}".format(str(e)))


def get_key_map_no_uid(user_id, keymap_alias, collection):
    result = run_query(GET_KEYMAP.format(collection = collection), (user_id, keymap_alias,))
    return '{"keymap_alias": "%s", "keymap": %s}' % (keymap_alias, json.dumps(_keymap_or_empty(result), ensure_ascii=False))  # Unpack list of tuples


def get_key_map(user_id, keymap_alias, collection):
    result = run_query(GET_KEYMAP_AND_ID.format(collection = collection), (user_id, keymap_alias,))
    return '{"user_id": "%s", "keymap_alias": "%s", "keymap": %s}' % (user_id, keymap_alias, json.dumps(_keymap_or_empty(result), ensure_ascii=False)) # Deal with empty list?


def get_key_maps(user_id, collection):
    result = run_query(GET_KEYMAPS.format(collection = collection), (user_id,))
    return json.dumps([{'keymap_alias': r[0]} for r in result], ensure_ascii=False)


def save_key_map(keymap, collection):
    keymap_json = json.dumps(keymap.keymap, ensure_ascii=False)
    result = run_query(INSERT_OR_UPDATE_KEYMAP.format(collection = collection), (keymap.user_id, keymap.keymap_alias, keymap_json, keymap_json,), False)
    return result


def delete_key_map(user_id, keymap_alias, collection):
    result = run_query(DELETE_KEYMAP.format(collection = collection), (user_id, keymap_alias,), False)
    return result

def _keymap_or_empty(result):
    try:
        return result[0][0]
    except IndexError:
        return []




