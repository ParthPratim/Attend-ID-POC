from bigchaindb.asset_templates.orgs_assets import ASSET_LIST
from bigchaindb.utils.assets import Asset
from bigchaindb.asset.create import CreateAsset
from bigchaindb.asset.transfer import TransferAsset
from bigchaindb.utils.connect import connect

class AssetsManager:
    def __init__(self,action,asset_data=None,c_keys=None,bdb=None,asset_id=None,p_keys=None):
        self.action = action
        self.bdb = bdb
        if self.action == "CREATE":
            asset =  Asset(ASSET_LIST,asset_data['asset_type'])
            asset.fill_placeholders(asset_data['values'])
            self.asset_data = asset.asset
            self.keys = c_keys
        elif self.action == "TRANSFER":
            self.asset_id = asset_id
            self.c_keys = c_keys
            self.p_keys = p_keys

    def create(self):
        txid = CreateAsset(self.bdb,self.asset_data,self.keys)
        return txid
    def transfer(self):
        
        txid = TransferAsset(self.bdb,self.asset_id,self.p_keys,self.c_keys);
        return txid
    @staticmethod
    def lookup_asset(bdb,sitem):
        return bdb.assets.get(search=sitem)

    @staticmethod
    def lookup_transactions(bdb,aid):
        return bdb.transactions.get(asset_id=aid)

    @staticmethod
    def get_from_id(bdb,aid):
        block_height = bdb.blocks.get(txid=aid)
        block = bdb.blocks.retrieve(str(block_height))['transactions'][0]
        return block
