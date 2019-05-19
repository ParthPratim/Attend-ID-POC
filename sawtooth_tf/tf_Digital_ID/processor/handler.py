from sawtooth_sdk.processor.handler import TransactionHandler
from processor.payload import DigitalIDPayload
import processor.transaction as txhandler
import hashlib


DIGITAL_ID_ADDRESS_PREFIX = hashlib.sha512("digital_id".encode('utf-8')).hexdigest()[0:6]

class tf_Digital_ID(TransactionHandler):
    @property
    def family_name(self):
        return 'digital_id'

    @property
    def family_versions(self):
        return ['1.1']

    @property
    def namespaces(self):
        return [DIGITAL_ID_ADDRESS_PREFIX]

    def apply(self,transaction,context):
        header = transaction.header
        payload = DigitalIDPayload(payload=transaction.payload)
        t_handler = txhandler.TransactionHandler(payload,context=context)
        t_handler.process()
