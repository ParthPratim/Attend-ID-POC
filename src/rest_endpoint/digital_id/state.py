import hashlib

class OrgsStateAddress:
    def __init__(self,hash):
        self.addr = hash
    @staticmethod
    def sha512(msg):
        return hashlib.sha512(msg.encode('utf-8')).hexdigest()
    @staticmethod
    def for_new_user(digital_id):
        digital_id_hash = hashlib.sha512(digital_id.encode('utf-8')).hexdigest()[-64:]
        return OrgsStateAddress(OrgsStateAddress.sha512("digital_id")[0:6]+digital_id_hash)
    @property
    def address(self):
        return self.addr
