from bigchaindb_driver import BigchainDB
bdb_root_url = 'http://bigchaindb:9984'

def connect():
    bdb = BigchainDB(bdb_root_url)
    return bdb
