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
            state_address = StateHelper(self._tx_payload.digital_id).state_address
            state_data = {
                "Name" : self._tx_payload.uname,
                "DigitalID" : self._tx_payload.digital_id
            }
            formatted_data = TransactionHandler.serialize(state_data)
            self._context.set_state({
                state_address : formatted_data
            }, timeout=3
            )

    @staticmethod
    def serialize(org_data):
        return cbor.dumps(org_data)