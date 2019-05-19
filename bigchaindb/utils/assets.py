from bigchaindb.asset_templates import orgs_assets
from bigchaindb.asset_templates import attend_assets

ASSET_LIST = {**orgs_assets.ASSET_LIST,**attend_assets.ASSET_LIST}
class Asset:
    def __init__(self,asset_dict,asset_type):
        self.asset_type = asset_type
        self.t_copy = ASSET_LIST[self.asset_type]

    def fill_placeholders(self,p_data):
        for field,val in p_data.items():
            self.t_copy["data"][field] = val

    @property
    def asset(self):
        return self.t_copy
