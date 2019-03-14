import cbor
from sawtooth_sdk.processor.exceptions import InvalidTransaction

class OrgsPayload:
    def __init__(self,payload=""):
        try:
            data = cbor.loads(payload)
            action = data['action']
            org_name = data['org_name']
            creator_id = data['creator_id']
            org_id = data['org_id']
        except ValueError:
            raise InvalidTransaction("Incorrect Data Serialization")
        if not action:
            raise InvalidTransaction("Action not specified")
        if not org_name:
            raise InvalidTransaction("Organization Name not specified")
        if not creator_id:
            raise InvalidTransaction("Organization creator's DigitalID not specified")
        if not org_id:
            raise InvalidTransaction("Organization creator's Organizatin ID not specified")
        if action not in ["create"]:
            raise InvalidTransaction("Action submitted is not supported")
        self._action = action
        self._org_name = org_name
        self._creator_id = creator_id
        self._org_id = org_id
    
    @property
    def action(self):
        return self._action
    @property
    def org_name(self):
        return self._org_name
    @property
    def creator_id(self):
        return self._creator_id
    @property
    def org_id(self):
        return self._org_id
