from bigchaindb.utils.helper import AssetsManager
from bigchaindb.utils.connect import connect
from rest_endpoint.digital_id.state import DigitalIDStateAddress
from rest_endpoint.internals.get_state_data import GetStateData

class OrgsAssets:

    @staticmethod
    def NewMember(did,keys):
        bdb = connect()
        lookup = AssetsManager.lookup_asset(bdb,"NewOrgMember")
        already_regs = False
        for item in lookup:
            block = AssetsManager.get_from_id(bdb,item['id'])
            transactions = AssetsManager.lookup_transactions(bdb,item['id'])
            transaction = transactions[len(transactions)-1]
            owner_pk = transaction['outputs'][0]['public_keys'][0]
            mdi = transactions[0]['asset']['data']['MemberDigitalID']
            if mdi == did:
                if owner_pk == keys.public_key:
                    already_regs = True
                    break

        if not already_regs:
            am = AssetsManager("CREATE",asset_data={
                "asset_type" : "NewMember",
                "values" : {
                    "MemberDigitalID" : did
                    }
                },c_keys=keys,bdb=bdb)

            return am.create()

        return False

    @staticmethod
    def TransferMember(asset_id,prevu_key,curru_key):
        bdb = connect()
        am = AssetsManager("TRANSFER",asset_id=asset_id,p_keys=prevu_key,c_keys=curru_key,bdb=bdb)
        return am.transfer()

    @staticmethod
    def GetOrgMemberList(org_keys):
        bdb = connect()
        lookup = AssetsManager.lookup_asset(bdb,"NewOrgMember")
        already_regs = False
        member_ids = []
        for item in lookup:
            block = AssetsManager.get_from_id(bdb,item['id'])
            transactions = AssetsManager.lookup_transactions(bdb,item['id'])
            transaction = transactions[len(transactions)-1]
            owner_pk = transaction['outputs'][0]['public_keys'][0]
            mdi = transactions[0]['asset']['data']['MemberDigitalID']
            if owner_pk == org_keys.public_key:
                state_addr = DigitalIDStateAddress.for_new_user(mdi).address
                data =  GetStateData(state_addr)
                member_ids.append((data['Name'],mdi))

        return member_ids


    @staticmethod
    def GetAssetID(digital_id,owner_keys):
        bdb = connect()
        lookup = AssetsManager.lookup_asset(bdb,digital_id)
        for asset in lookup:
            if asset['data']['AssetType'] == "NewOrgMember":
                transactions = AssetsManager.lookup_transactions(bdb,asset['id'])
                transaction = transactions[len(transactions)-1]
                if transaction['outputs'][0]['public_keys'][0] == owner_keys.public_key:
                    return asset['id']

        return False
