import hashlib

class StateHelper:
    def __init__(self,org_id,creator_id):
        base = hashlib.sha512("orgs".encode('utf-8')).hexdigest()[0:6]
        org_hash = hashlib.sha512(org_id.encode('utf-8')).hexdigest()[-32:]
        creator_hash = hashlib.sha512(creator_id.encode('utf-8')).hexdigest()[-32:]
        self._state_address = base+org_hash+creator_hash

    def helper_type(self):
        return "ORGS_TP_STATE_HELPER"
        
    @property
    def state_address(self):
        return self._state_address