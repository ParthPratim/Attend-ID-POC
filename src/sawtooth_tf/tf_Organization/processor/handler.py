from sawtooth_sdk.processor.handler import TransactionHandler
from processor.payload import OrgsPayload
from processor.transaction import TransactionHandler
import hashlib

class tf_Organization(TransactionHandler) :
    @property
    def family_name(self):
        return 'orgs'

    @property
    def family_versions(self):
        return ['1.0']

    @property
    def namespaces(self):
        return [ORG_ADDRESS_PREFIX]

    def apply(self, transaction, context):
        header = transaction.header
        payload = OrgsPayload(payload=transaction.payload)
        t_handler = TransactionHandler(payload,context=context)
        t_handler.process()
        print("DONE")
