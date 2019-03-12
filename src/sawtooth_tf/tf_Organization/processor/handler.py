from sawtooth_sdk.processor.handler import TransactionHandler
from processor.payload import OrgsPayload
import hashlib

 
ORG_ADDRESS_PREFIX = hashlib.sha512("orgs".encode('utf-8')).hexdigest()[0:6]

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
        payload = OrgsPayload(payload=transaction.payload,context=context)
        
