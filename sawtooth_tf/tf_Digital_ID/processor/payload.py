import cbor
from sawtooth_sdk.processor.exceptions import InvalidTransaction

class DigitalIDPayload:
    def __init__(self,payload=""):
        try:
            data = cbor.loads(payload)
            action = data['action']
            uname = data['uname']
            digital_id = data['digital_id']
            bdb_pub_key = ""
            bdb_priv_key = ""
            certificate_hash = ""
            training_image_hash = ""
            access_token = ""

        except ValueError:
            raise InvalidTransaction("Incorrect data serialization")
        if not action:
            raise InvalidTransaction("Action not specified")
        if not uname:
            raise InvalidTransaction("Username not provided")
        if not digital_id:
            raise InvalidTransaction("Digital ID not computed")
        if action not in ["create","new_token"]:
            raise InvalidTransaction("Action not supported")
        if "access_token" in data:
            access_token = data['access_token']
        if "bdb_pub_key" in data:
            bdb_pub_key = data['bdb_pub_key']
        if "bdb_priv_key" in data:
            bdb_priv_key = data['bdb_prib_key']
        if "certificate_hash" in data:
            certificate_hash = data['certificate_hash']
        if "training_image_hash" in data:
            training_image_hash = data['training_image_hash']

        self._action = action
        self._digital_id = digital_id
        self._uname = uname
        self._bdb_pub_key = bdb_pub_key
        self._bdb_priv_key = bdb_priv_key
        self._certificate_hash = certificate_hash
        self._training_image_hash = training_image_hash
        self._access_token = access_token

    @property
    def action(self):
        return self._action

    @property
    def uname(self):
        return self._uname

    @property
    def digital_id(self):
        return self._digital_id

    @property
    def bdb_key_pair(self):
        return (self._bdb_pub_key,self._bdb_priv_key)

    @property
    def certificate_hash(self):
        return self._certificate_hash

    @property
    def training_image_hash(self):
        return self._training_image_hash

    @property
    def access_token(self):
        return self._access_token
