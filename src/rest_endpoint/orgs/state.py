import hashlib

class OrgsStateAddress:
    def __init__(self,hash):
        self.addr = hash
    @staticmethod
    def sha512(msg):
        return hashlib.sha512(msg.encode('utf-8')).hexdigest()
    @staticmethod
    def for_new_org(org_id,creator_id):
        org_hash = hashlib.sha512(org_id.encode('utf-8')).hexdigest()[-32:]
        creator_hash = hashlib.sha512(creator_id.encode('utf-8')).hexdigest()[-32:]
        return OrgsStateAddress(OrgsStateAddress.sha512("orgs")[0:6]+org_hash+creator_hash)
    @property
    def address(self):
        return self.addr
