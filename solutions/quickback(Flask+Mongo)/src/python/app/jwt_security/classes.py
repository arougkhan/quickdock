import json

class Usermodel:
    def __init__(self, subject=None, user_id=None, group_id=None, org_id=None, displayname=None, username=None, authorities=None):
        self.subject = subject
        self.user_id = user_id
        self.group_id = group_id
        self.org_id = org_id
        self.displayname = displayname
        self.username = username
        self.authorities = authorities or []

    @staticmethod
    def load_from_jwt(jwt_payload):
        return Usermodel(jwt_payload["sub"], jwt_payload["user_id"],jwt_payload["group_id"], jwt_payload["org_id"],
                         jwt_payload["username"], jwt_payload["displayname"], Usermodel.extract_roles(jwt_payload))

    # Don't bother prefixing with "ROLE_". This. Is. NotSpring! All roles get dumped into the same bucket.
    @staticmethod
    def extract_roles(jwt_payload):
        return jwt_payload["realm_access"]["roles"] + jwt_payload["resource_access"]["account"]["roles"]

    #@staticmethod
    #def from_json(json_data):
    #    record = json.loads(json_data)
    #    if record is None:
    #        return Keymap.empty_map()
    #    return Keymap(**rescord)