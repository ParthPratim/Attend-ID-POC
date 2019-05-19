from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from bigchaindb_driver.crypto import generate_keypair

class Key:
    def __init__(self,pub,priv):
        self.pub = pub
        self.priv = priv

    @property
    def public_key(self):
        return self.pub

    @property
    def private_key(self):
        return self.priv

class GenerateRandomKeyPair:
    @staticmethod
    def create():
        #context = create_context('secp256k1')
        #private_key = context.new_random_private_key()
        #signer = CryptoFactory(context).new_signer(private_key)
        key_pair = generate_keypair()
        return {'pub_key':key_pair.public_key , 'priv_key':key_pair.private_key}
