# SAWTOOTH TX STUB
import cbor
import os
from hashlib import sha512
from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
from tornado.httpclient import AsyncHTTPClient
import urllib.request
from urllib.error import HTTPError

SAWTOOTH_REST_API_ENDPOINT = "http://localhost:4000/batches"

class SawtoothClientStub:
    def __init__(self, tf_name="", tf_version="1.0", payload = {}):
        self._payload = payload
        self.tf_name = tf_name
        self.tf_version = tf_version
    
    def set_address_scope(self,inputs=[],outputs=[]):
        self._inputs = inputs
        self._outputs = outputs
    
    def load_keys(self):
        context = create_context('secp256k1')
        self._priv_key = open("/genesis-hack/keys/rest_client/private.key").read()
        self.signer = CryptoFactory(context).new_signer(Secp256k1PrivateKey.from_hex(self._priv_key))

    def txn_header_gen(self):
        self.load_keys()
        self.payload_bytes = cbor.dumps(self._payload)

        self.txn_header_bytes = TransactionHeader(
            family_name=self.tf_name,
            family_version=self.tf_version,
            inputs=self._inputs,
            outputs=self._outputs,
            signer_public_key=self.signer.get_public_key().as_hex(),
            batcher_public_key=self.signer.get_public_key().as_hex(),
            dependencies=[],
            payload_sha512=sha512(self.payload_bytes).hexdigest()
            ).SerializeToString()
    
    def create_txn(self):
        signature = self.signer.sign(self.txn_header_bytes) 
        txn = Transaction(
            header=self.txn_header_bytes,
            header_signature=signature,
            payload=self.payload_bytes
            )
        self.txns = [txn]
    
    def create_batch(self):
        batch_header_bytes = BatchHeader(
            signer_public_key=self.signer.get_public_key().as_hex(),
            transaction_ids=[txn.header_signature for txn in self.txns],
            ).SerializeToString()
    
        signature = self.signer.sign(batch_header_bytes)

        batch = Batch(
            header=batch_header_bytes,
            header_signature=signature,
            transactions=self.txns
            )

        self.batch_list_bytes = BatchList(batches=[batch]).SerializeToString()
    
    def prepare_tx_batch(self):
        self.txn_header_gen()
        self.create_txn()
        self.create_batch()
    
    def send(self):
        try:
            request = urllib.request.Request(
                'http://sawtooth-0:8008/batches',
                self.batch_list_bytes,
                method='POST',
                headers={'Content-Type': 'application/octet-stream'})
            response = urllib.request.urlopen(request)
        except HTTPError as e:
            response = e.file
    