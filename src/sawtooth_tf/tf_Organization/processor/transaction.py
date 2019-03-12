import secrets
import hashlib
from processor.state import StateHelper

class TransactionHandler:
    def __init__(self,tx_payload):
        self._tx_payload = tx_payload
    def process(self):
        if self._tx_payload == "create":
            org_id = self.compute_random_org_id()
            state_addr = StateHelper(org_id,self._tx_payload.creator_id)
            
            pass;