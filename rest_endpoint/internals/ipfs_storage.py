import ipfshttpclient
from OpenSSL import crypto

class IpfsStorage:

    def __init__(self,hash=None):
        self._fhash = hash
        self.ipfs_conn = ipfshttpclient.connect(host="ipfs-net")

    @property
    def hash(self):
        return self._fhash

    def store_json(self,json_data):
        uhash = self.ipfs_conn.add_json(json_data)['Hash']
        self._fhash = uhash
        return uhash

    def store_file(self,file_path):
        uhash = self.ipfs_conn.add(file_path)['Hash']
        self._fhash = uhash
        return uhash

    def store_bytes(self,data):
        uhash = self.ipfs_conn.add_bytes(data)
        self._fhash = uhash
        return uhash

    def store_pyobj(self,data):
        uhash = self.ipfs_conn.add_pyobj(data)
        self._fhash = uhash
        return uhash

    @staticmethod
    def from_hash(hash):
        return IpfsStorage(hash)

    def load_contents(self):
        contents = self.ipfs_conn.cat(self._fhash)
        return contents

"""
fs = IpfsStorage()
hash = fs.store_file("server.p12")['Hash']
print(hash)
fs = IpfsStorage.from_hash(hash)
data = fs.load_contents()
p12 = crypto.load_pkcs12(data)
if open("../../keys/ssl/server.pem","rb").read() == crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate()):
    print("YEAH...ITS THE SAME...")
"""
