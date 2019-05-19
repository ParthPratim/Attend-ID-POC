from bigchaindb_driver import BigchainDB
bdb_root_url = 'https://example.com:9984'  # Use YOUR BigchainDB Root URL here
bdb = BigchainDB(bdb_root_url)
bicycle = {
        'data': {
            'Parth': {
                'type' : 'Organization',
                'serial_number': 'abcd1234',
                'manufacturer': 'bkfab',
            },
        },
    }
metadata = {'planet': 'earth'}

from bigchaindb_driver.crypto import generate_keypair
