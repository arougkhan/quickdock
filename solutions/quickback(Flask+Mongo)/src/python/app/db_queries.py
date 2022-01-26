from pymongo import MongoClient
from bson.json_util import dumps
from config import mongo_config as config
import sys
from pprint import pprint

client = MongoClient(config['db_connection'])
# Define database
db = client.keymap
# Define database "tables"
custom_maps = db.custommaps
base_maps = db.basemaps


def get_key_map_no_uid(user_id, keymap_alias, collection):
    return dumps(next(iter(collection.find({'user_id': user_id, 'keymap_alias': keymap_alias}, {'_id': 0, 'user_id': 0})), None), ensure_ascii=False)


def get_key_map(user_id, keymap_alias, collection):
    return dumps(next(iter(collection.find({'user_id': user_id, 'keymap_alias': keymap_alias}, {'_id': 0})), None), ensure_ascii=False)


def get_key_maps(user_id, collection):
    return dumps(collection.find({'user_id': user_id}, {'keymap_alias': 1, '_id': 0}), ensure_ascii=False)


def save_key_map(keymap, collection):
    return insert_or_update(keymap, collection)


def delete_key_map(user_id, keymap_alias, collection):
    collection.delete_one({'user_id': user_id, 'keymap_alias': keymap_alias})
    return "Record deleted"


# Utility functions
def insert_or_update(keymap, collection):
    collection.replace_one(
        keymap.id_key(),
        vars(keymap), True)
    return "Record updated"




