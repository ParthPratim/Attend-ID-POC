from bigchaindb.utils.helper import AssetsManager
from bigchaindb.utils.connect import connect
import hmac
import datetime
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
                "SessionID" : session_id,
                "CreationDate" : datetime.datetime.now().strftime('%d/%m/%y'),
                "CreationTime" : datetime.datetime.now().strftime('%H:%M')
            }
        }, c_keys=keys, bdb=bdb)

        return (am.create(),session_id)

    @staticmethod
    def MarkPresence(sess_id,m_did,keys):
        bdb = connect()
        can_proceed = False
        lookup = AssetsManager.lookup_asset(bdb,"NewAttendanceSession")
        for entry in lookup:
            if entry['data']['AssetType'] == 'NewAttendanceSession' :
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

            dx = am.create()
            print(dx)
            return dx
        else:
            return can_proceed

    @staticmethod
    def GetSessionList(initiator):
        bdb = connect()
        lookup = AssetsManager.lookup_asset(bdb,"NewAttendanceSession")
        session_list = []
        session_ids = []
        presents = {}
        for entry in lookup:
            if entry['data']['AssetType'] == 'NewAttendanceSession' :
                if entry['data']['SessionInitiator'] == initiator:
                    session_ids.append(entry['data']['SessionID'])
                    presents[entry['data']['SessionID']] = 0
                    session_list.append({
                        "Name" : entry['data']['SessionName'] ,
                        "Date"  : entry['data']['CreationDate'],
                        "Time" : entry['data']['CreationTime'],
                        "Present" : "0"
                        })

        lookup2 = AssetsManager.lookup_asset(bdb,"SessionPresence")
        print(lookup2)
        for entry in lookup2:
            if entry['data']['AssetType'] == 'SessionPresence' :
                id = entry['data']['SessionID']
                if id in session_ids:
                    presents[id] = presents[id] + 1
        index = 0
        for session_id in session_ids:
            session_list[index]['Present'] = presents[session_id]
            index = index + 1

        return session_list[::-1]
