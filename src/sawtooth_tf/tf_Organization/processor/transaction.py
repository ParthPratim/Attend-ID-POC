import hashlib
import cbor
import logging
from processor.state import StateHelper

class TransactionHandler:
    def __init__(self,tx_payload,context=None):
        self._tx_payload = tx_payload
        self._context = context
    def process(self):
        if self._tx_payload.action == "create":
            state_addr = StateHelper(self._tx_payload.org_id,self._tx_payload.creator_id).state_address
            state_data = {
                'Organization' : self._tx_payload.org_name,
                'CreatorID' : self._tx_payload.creator_id,
                'OrgID' : self._tx_payload.org_id
            }
            formatted_data = TransactionHandler.serialize(state_data)
            print(formatted_data)
            print(state_addr)
            self._context.set_state(
                {
                    state_addr : formatted_data
                }, 
                timeout=3
            )

    @staticmethod
    def serialize(org_data):
        return cbor.dumps(org_data)

    @staticmethod
    def deserialize(cbor_data):
        return cbor.loads(cbor_data)

