import tornado.web
import cv2
import numpy as np
import hmac
import hashlib
import pickle
import tornado.escape
from PIL import Image
from io import BytesIO
from tornado.web import HTTPError
from rest_endpoint.digital_id.state import DigitalIDStateAddress
from rest_endpoint.orgs.state import OrgsStateAddress
from rest_endpoint.internals.get_state_data import GetStateData
from rest_endpoint.internals.ipfs_storage import IpfsStorage
#from facenet.face_recognition_image import RecognizeFace
from fre_layer.azure_cloud import RecognizeFace
from rest_endpoint.sawtooth_client.tx import SawtoothClientStub
from rest_endpoint.internals.ssl_auth import *
from bigchaindb.asset_logic.attendance import AttendanceAssets
from bigchaindb.utils.bdb_ukey import Key

class OrgWhoisItHandler(tornado.web.RequestHandler):

    def post(self):
        files = self.request.files['images']
        payload = {}
        payload['org_id'] = self.get_body_argument("org_id", default=None, strip=False)
        payload['sess_id'] = self.get_body_argument("sess_id", default=None, strip=False)
        if payload['sess_id'] == None or payload['org_id'] == None or len(files) == 0:
            self.write({
                "error" : "Malformed Request"
            })
            self.finish()
            return
        ufile = files[0]
        raw_imgs = []
        img = Image.open(BytesIO(ufile['body']))
        pixels = list(img.getdata())
        width, height = img.size
        pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
        np_img = np.array(pixels,dtype=np.uint8)
        raw_imgs.append(cv2.cvtColor(np_img, cv2.COLOR_BGR2RGB))
        state_addr = OrgsStateAddress.for_new_org(payload['org_id'],"PADDING_TEXT_IGNORED").address
        s_data = GetStateData(state_addr)
        if s_data == False:
            self.write({
                "error" : "Invalid Organization Name"
            })
            self.finish()
            return
        else:
            '''
            FRModel_hash = s_data['FRModel']
            if FRModel_hash == "":
                self.write({
                    "error" : "First Train the org Model using the web dashboard",
                })
                self.finish()
                return

            (model,class_names) = pickle.loads(IpfsStorage.from_hash(FRModel_hash).load_contents())
            '''
            probable = RecognizeFace(raw_imgs)
            if probable != None:
                if len(probable) > 0 :
                    prob_did = probable[0]
                    dsa = GetStateData(DigitalIDStateAddress.for_new_user(prob_did).address)
                    if dsa == False:
                        self.write({
                            "error" : "Internal Error"
                        })
                        self.finish()
                        return
                    if payload['org_id'] not in dsa['Organizations'] :
                        self.write({
                            "error" : "You don't belong to this Organization. Get Lost you Spoofer !"
                        })
                        self.finish()
                        return
                    else:
                        response = AttendanceAssets.MarkPresence(payload['sess_id'],prob_did,Key(dsa['BDB_pub_key'],dsa['BDB_priv_key']))
                        if response == False:
                            self.write({
                                "error" : "Invalid SessionID. Please don't spoof. You simply can't !!!"
                            })
                            self.finish()
                            return
                        else:
                            self.write({
                                "status" : "Marked Your Attendance.",
                                "code" : "ATTENDANCE_MARKED",
                                "did" : prob_did,
                                "name" : dsa['Name']
                            })
                            self.finish()
                            return
            self.write({
                "error" : "You don't belong to this organization. What are you doing here bro !!!"
            })
            self.finish()

class AttendanceSession(tornado.web.RequestHandler):

    def post(self):
        payload = tornado.escape.json_decode(self.request.body)
        if "org_id" not in payload or "sess_name" not in payload or "sess_ini_did" not in payload:
            self.write({
                "error" : "Malformed Request"
            })
            self.finish()
            return

        payload['sess_name'] = payload['sess_name'].strip()

        if len(payload['sess_name']) == 0 :
            self.write({
                "error" : "Invalid Session Name."
            })
            self.finish()
            return
        else:
            osda = GetStateData(OrgsStateAddress.for_new_org(payload['org_id'],"PADDING_TEXT_IGNORED").address)
            if osda == False:
                self.write({
                    "error" : "Invalid Organizaition Name"
                })
                self.finish()
                return
            else:
                dsda = GetStateData(DigitalIDStateAddress.for_new_user(payload['sess_ini_did']).address)
                if dsda == False or dsda['CanMarkAttendance'] == False or payload['org_id'] not in dsda['Organizations']:
                    self.write({
                        "error" : "Invalid Session Creator, does not have attendance marking privilidge or does not belong to this organization. Please stop spoofing this is a POC"
                    })
                    self.finish()
                    return
                else:
                    status , session_id = AttendanceAssets.NewSession(payload['sess_name'],payload['sess_ini_did'],payload['org_id'],Key(dsda['BDB_pub_key'],dsda['BDB_priv_key']))
                    if status == False:
                        self.write({
                            "error" : "Internal Failure..."
                        })
                        self.finish()
                        return
                    else:
                        self.write({
                            "SessionID" : session_id
                        })
                        self.finish()
                        return

class SessionList(tornado.web.RequestHandler):

    def get(self):
        payload = tornado.escape.json_decode(self.request.body)

        if "initiator" not in payload:
            self.write({
                "error" : "No Session Initiator mentioned !!!"
            })
            self.finish()
            return
        print("Getting Session List...")

        sess_list = AttendanceAssets.GetSessionList(payload['initiator'])
        print(sess_list)
        if len(sess_list) == 0 :
            self.write({
                "error" : "No Session Entries Found for This Session Initiator"
            })
            self.finish()
        else:
            self.write({
                "Sessions" : sess_list
            })
            self.finish()
