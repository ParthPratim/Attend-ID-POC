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
            new_member_id = ""
            new_org_id = ""
            curr_member_id = ""
            new_org_creator = ""
            certificate_hash = ""
            can_mark_attendance = "False"
            bdb_pub_key = ""
            bdb_priv_key = ""
            frmodel = ""

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
        if "new_member_id" in data:
            new_member_id = data['new_member_id']
        if "new_org_id" in data:
            new_org_id = data['new_org_id']
        if "curr_member_id" in data:
            curr_member_id = data['curr_member_id']
        if "new_org_creator" in data:
            new_org_creator = data['new_org_creator']
        if "certificate_hash" in data:
            certificate_hash = data['certificate_hash']
        if "can_mark_attendance" in data:
            can_mark_attendance = data['can_mark_attendance']
        if "bdb_pub_key" in data:
            bdb_pub_key = data['bdb_pub_key']
        if "bdb_priv_key" in data:
            bdb_priv_key = data['bdb_priv_key']
        if "frmodel" in data:
            frmodel = data['frmodel']
        self._action = action
        self._org_name = org_name
        self._creator_id = creator_id
        self._org_id = org_id
        self._new_member_id = new_member_id
        self._new_org_id = new_org_id
        self._curr_member_id = curr_member_id
        self._new_org_creator = new_org_creator
        self._certificate_hash = certificate_hash
        self._can_mark_attendance = can_mark_attendance
        self._bdb_pub_key = bdb_pub_key
        self._bdb_priv_key = bdb_priv_key
        self._frmodel = frmodel

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
    @property
    def new_member_id(self):
        return self._new_member_id
    @property
    def new_org_id(self):
        return self._new_org_id
    @property
    def curr_member_id(self):
        return self._curr_member_id
    @property
    def new_org_creator(self):
        return self._new_org_creator
    @property
    def certificate_hash(self):
        return self._certificate_hash
    @property
    def can_mark_attendance(self):
        return self._can_mark_attendance
    @property
    def bdb_keys(self):
        return (self._bdb_pub_key,self._bdb_priv_key)
    @property
    def frmodel(self):
        return self._frmodel
