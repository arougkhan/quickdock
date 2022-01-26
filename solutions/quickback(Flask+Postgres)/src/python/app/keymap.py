import json
#import bson.json_util as _bson


class Keymap:
    def __init__(self, user_id=None, keymap_alias=None, keymap=None):
        self.user_id = user_id
        self.keymap_alias = keymap_alias or 'default'
        self.keymap = keymap or []

    def id_key(self):
        return {'keymap_alias': self.keymap_alias, 'user_id': self.user_id}

    @staticmethod
    def empty_map():
        return Keymap('Error:[not_found/invalid]', 'Error:[not_found/invalid]', [])

    @staticmethod
    def from_json(json_data):
        record = json.loads(json_data)
        if record is None:
            return Keymap.empty_map()
        return Keymap(**record)

#   @staticmethod
#   def from_bson(bson_data):
#       record = _bson.loads(bson_data)
#       if record is None:
#           return Keymap.empty_map()
#       return Keymap(**record)

