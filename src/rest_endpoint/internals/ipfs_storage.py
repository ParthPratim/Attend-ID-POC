import ipfsapi

class IpfsStorgae:

    def __init__(self,hash=None):
        self._fhash = hash
        self.ipfs_conn = ipfsapi.connect()

    @property
    def hash(self):
        return self._fhash

    def store_json(self,json_data):
        uhash = self.ipfs_conn.add_json(json_data)
        self._fhash = uhash
        return uhash
    
    def store_file(self,file_path):
        uhash = self.ipfs_conn.add(file_path)
        self._fhash = uhash
        return uhash

    @staticmethod
    def from_hash(hash):
        return IpfsStorgae(hash)
    
    def load_contents(self):
        contents = self.ipfs_conn.cat(self._fhash)
        return contents