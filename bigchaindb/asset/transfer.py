def get_from_id(bdb,aid):
    block_height = bdb.blocks.get(txid=aid)
    block = bdb.blocks.retrieve(str(block_height))['transactions'][0]
    return block

def TransferAsset(bdb,asset_id,prevu_key,curru_key):
    lis = bdb.transactions.get(asset_id=asset_id)
    creation_tx = lis[0]

    transfer_tx = lis[len(lis)-1]
    #bdb.transactions.get(asset_id=asset_id,operation="TRANSFER")
    if transfer_tx == creation_tx :
        transfer_asset = {
            'id': transfer_tx['id'],
            }
    else:
        transfer_asset = {
            'id': transfer_tx['asset']['id'],
            }

    if transfer_tx['outputs'][0]['public_keys'][0] == prevu_key.public_key:
        #initiate transfer
        print(creation_tx)
        print(transfer_tx)

        output = creation_tx['outputs'][0]

        transfer_input = {
            'fulfillment': output['condition']['details'],
            'fulfills': {
                'output_index': 0,
                'transaction_id': transfer_tx['id'],
                },
            'owners_before': [prevu_key.public_key]
            }

        prepared_transfer_tx_again = bdb.transactions.prepare(
            operation='TRANSFER',
            asset=transfer_asset,
            inputs=transfer_input,
            recipients=curru_key.public_key,)
        # Fulfillment of transfer
        fulfilled_transfer_tx_again = bdb.transactions.fulfill(
            prepared_transfer_tx_again,
            private_keys=prevu_key.private_key,)
        # Send it across the Node
        sent_transfer_tx_again = bdb.transactions.send_commit(fulfilled_transfer_tx_again)
        return sent_transfer_tx_again['id']
    else:
        return False
