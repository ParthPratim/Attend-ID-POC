import hashlib

class StateHelper:
    def __init__(self,digital_id):
        base = hashlib.sha512("digital_id".encode('utf-8')).hexdigest()[0:6]
        creator_id_hash = hashlib.sha512(digital_id.encode('utf-8')).hexdigest()[-64:]
        self._state_address = base+creator_id_hash

    def helper_type(self):
        return "DIGITAL_ID_TP_STATE_HELPER"

    @property
    def state_address(self):
        return self._state_address
