
def CreateAsset(bdb,asset,keys):

    prepared_creation_tx = bdb.transactions.prepare(operation='CREATE',
                                                    signers=keys.public_key,
                                                    asset=asset)

    fulfilled_creation_tx = bdb.transactions.fulfill(prepared_creation_tx,
                                                 private_keys=keys.private_key)

    sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)

    txid = fulfilled_creation_tx['id']

    return txid
