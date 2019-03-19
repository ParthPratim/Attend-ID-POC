import Crypto
import base64
import os
import json
import ipfsapi.client
import ipfsapi.client
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS
from rest_endpoint.internals.ipfs_storage import IpfsStorage
from rest_endpoint.internals.general import hex_to_bytes

class IdentityKeyDriver:
    def __init__(self,private_key,public_key):
        self._private_key = private_key
        self._public_key = public_key
        self._private_key_PEM = self._public_key_PEM = None
    
    @staticmethod
    def new_rsa_key_pair():
        KEY_BYTES = 2048
        private_key = RSA.generate(2048)
        public_key = private_key.publickey()
        return IdentityKeyDriver(private_key,public_key)
    
    @staticmethod
    def from_rsa_key_pair(priv_key,pub_key):
        return IdentityKeyDriver(priv_key,pub_key)

    @staticmethod
    def from_RSA_key_pair_hex(priv_key,pub_key,digital_id):
        return IdentityKeyDriver.from_rsa_key_pair(
            RSA.importKey(hex_to_bytes(priv_key),passphrase=digital_id),
            RSA.importKey(hex_to_bytes(pub_key),passphrase=digital_id)
        )

    def create_digital_signature(self):
        random_payload = os.urandom(16).hex()
        hash = SHA256.new(random_payload.encode())
        padded_rsa_key = PKCS1_PSS.new(self._private_key)
        signature = padded_rsa_key.sign(hash)
        return (hash,signature)
    
    def verify_digital_signature(self,digi_sig):
        padded_rsa_key = PKCS1_PSS.new(self._public_key)
        return padded_rsa_key.verify(digi_sig[0],digi_sig[1])
    
    def export_to_PEM(self,digital_id,ktype="PRIVATE_KEY"):
        if ktype == "PRIVATE_KEY":
            self._private_key_PEM =  self._private_key.exportKey(format='PEM',passphrase=digital_id)
            return self._private_key_PEM
        elif ktype == "PUBLIC_KEY":
            self._public_key_PEM = self._public_key.exportKey(format='PEM',passphrase=digital_id)
            return self._public_key_PEM
        elif ktype == "PAIR":
            return (self.export_to_PEM(digital_id,"PRIVATE_KEY"),self.export_to_PEM(digital_id,"PUBLIC_KEY"))
    
    def read_PEM(self,pem_data,digital_id):
        return RSA.importKey(pem_data,passphrase=digital_id)

    @property
    def private_key(self):
        return self._private_key
    
    @property
    def public_key(self):
        return self._public_key
    
    def broadcast_keys(self):
        keys_json = {
            "PrivateKey" : self._private_key_PEM.hex(),
            "PublicKey" : self._public_key_PEM.hex()
        }
        ipfs = IpfsStorage()
        ipfs_hash = ipfs.store_json(keys_json)    
        return ipfs
    
    
#x = IdentityKeyDriver.new_rsa_key_pair()
#x.export_to_PEM("test_user","PAIR")
#ih = x.broadcast_keys()
#print(ih.hash)

""" f = IpfsStorgae(hash="QmSAthSEiK2rzyW5Ff4Vj26hQtMZLa5SUzDnpePPXyqdPA")
cont = f.load_contents()
json_d = json.loads(cont)
priv = json_d["PrivateKey"]
pub = json_d["PublicKey"]

f2 = IdentityKeyDriver.from_RSA_key_pair_hex(priv,pub)
d = f2.export_to_PEM("test_user","PAIR")

"""