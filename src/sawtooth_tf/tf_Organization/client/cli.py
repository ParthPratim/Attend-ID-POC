from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from hashlib import sha512
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
import cbor
import hashlib
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
import urllib.request
from urllib.error import HTTPError
from tornado.concurrent import Future

def cli_main():
    context = create_context('secp256k1')
    private_key = context.new_random_private_key()
    signer = CryptoFactory(context).new_signer(private_key)
    payload = {
    'Value': 42}

    payload_bytes = cbor.dumps(payload)

    txn_header_bytes = TransactionHeader(
    family_name='orgs',
    family_version='1.0',
    inputs=[],
    outputs=[hashlib.sha512("orgs".encode('utf-8')).hexdigest()[0:6] + hashlib.sha512("coder".encode('utf-8')).hexdigest()[-64:]],
    signer_public_key=signer.get_public_key().as_hex(),
    batcher_public_key=signer.get_public_key().as_hex(),
    dependencies=[],
    payload_sha512=sha512(payload_bytes).hexdigest()
    ).SerializeToString()

    signature = signer.sign(txn_header_bytes) 

    txn = Transaction(
    header=txn_header_bytes,
    header_signature=signature,
    payload=payload_bytes
    )

    txns = [txn]

    batch_header_bytes = BatchHeader(
    signer_public_key=signer.get_public_key().as_hex(),
    transaction_ids=[txn.header_signature for txn in txns],
    ).SerializeToString()
    
    signature = signer.sign(batch_header_bytes)

    batch = Batch(
    header=batch_header_bytes,
    header_signature=signature,
    transactions=txns
    )

    batch_list_bytes = BatchList(batches=[batch]).SerializeToString()
    output = open('orgs.batches', 'wb')
    output.write(batch_list_bytes)

