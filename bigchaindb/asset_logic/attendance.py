from bigchaindb.utils.helper import AssetsManager
from bigchaindb.utils.connect import connect
import hmac
import hashlib
import os

class AttendanceAssets:

    @staticmethod
    def NewSession(sess_name,sess_ini_did,org_id,keys):
        session_id = hmac.new(os.urandom(32).hex().encode('utf-8'),(sess_ini_did[:20]+org_id[-20:]).encode('utf-8'),hashlib.sha256).hexdigest()
        bdb = connect()
        am = AssetsManager("CREATE", asset_data={
            "asset_type" : "NewAttendanceSession",
            "values" : {
                "SessionName" : sess_name,
                "SessionInitiator" : sess_ini_did,
                "Organization" : org_id,
                "SessionID" : session_id
            }
        }, c_keys=keys, bdb=bdb)

        return (am.create(),session_id)

    @staticmethod
    def MarkPresence(sess_id,m_did,keys):
        bdb = connect()
        can_proceed = False
        lookup = AssetsManager.lookup_asset(bdb,"NewAttendanceSession")
        for entry in lookup:
            if entry['data']['SessionID'] ==  sess_id:
                can_proceed = True
                break
        if can_proceed:
            am = AssetsManager("CREATE",asset_data={
                "asset_type" : "Present",
                "values" : {
                    "MarkedFor" : m_did,
                    "SessionID" : sess_id
                }
            }, c_keys=keys, bdb=bdb)

            return am.create()
        else:
            return can_proceed
