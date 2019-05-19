import hashlib
import cbor
import logging
from processor.state import StateHelper


class TransactionHandler:
    def __init__(self,tx_payload,context=None):
        self._tx_payload = tx_payload
        self._context = context

    def process(self):
        print("REACHED")
        if self._tx_payload.action == "create":
            print("CREATING USER...")
            state_address = StateHelper(self._tx_payload.digital_id).state_address
            state_data = {
                "Name" : self._tx_payload.uname,
                "DigitalID" : self._tx_payload.digital_id,
                "BDB_pub_key" : self._tx_payload.bdb_key_pair[0],
                "BDB_priv_key" : self._tx_payload.bdb_key_pair[1],
                "Organizations" : [],
                "CertificateHash" : self._tx_payload.certificate_hash,
                "TrainingImageHash" : self._tx_payload.training_image_hash,
                "CanMarkAttendance" : False,
                "AccessToken" : ""
            }
            formatted_data = TransactionHandler.serialize(state_data)
            self._context.set_state({
                state_address : formatted_data
            }, timeout=3
            )
            print("ADDED USER...")

        elif self._tx_payload.action == "new_token" :
            print("CREATING ACCESS TOKEN...")
            state_address = StateHelper(self._tx_payload.digital_id).state_address
            state_entries = self._context.get_state(
                [state_address],
                timeout=3
            )
            state_data =  TransactionHandler.deserialize(state_entries[0].data)
            state_data['AccessToken'] = self._tx_payload.access_token
            formatted_data = TransactionHandler.serialize(state_data)
            self._context.set_state({
                state_address : formatted_data
            }, timeout=3
            )

    @staticmethod
    def serialize(org_data):
        return cbor.dumps(org_data)

    @staticmethod
    def deserialize(cbor_data):
        return cbor.loads(cbor_data)
