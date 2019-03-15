import cbor
from sawtooth_sdk.processor.exceptions import InvalidTransaction

class DigitalIDPayload:
    def __init__(self,payload=""):
        try:
            data = cbor.loads(payload)
            action = data['action']
            uname = data['uname']
            digital_id = data['digital_id']
        except ValueError:
            raise InvalidTransaction("Incorrect data serialization")
        if not action:
            raise InvalidTransaction("Action not specified")
        if not uname:
            raise InvalidTransaction("Username not provided")
        if not digital_id:
            raise InvalidTransaction("Digital ID not computed")
        if action not in ["create"]:
            raise InvalidTransaction("Action not supported")
        self._action = action
        self._uname = uname
        self._digital_id = digital_id
    
    @property
    def action(self):
        return self._action
    
    @property
    def uname(self):
        return self._uname

    @property
    def digital_id(self):
        return self._digital_id
