import tornado.web
import cv2
import numpy as np
import hmac
import hashlib
from PIL import Image
from io import BytesIO
from tornado.web import HTTPError
from rest_endpoint.digital_id.state import DigitalIDStateAddress
from rest_endpoint.orgs.state import OrgsStateAddress
from rest_endpoint.internals.get_state_data import GetStateData
#from facenet.face_recognition_image import RecognizeFace
from fre_layer.azure_cloud import RecognizeFace
from rest_endpoint.sawtooth_client.tx import SawtoothClientStub
from rest_endpoint.internals.ssl_auth import *

class GlobalWhoisItHandler(tornado.web.RequestHandler):

    def post(self):
        payload = { }
        raw_imgs = []
        ufile = self.request.files['images'][0]
        img = Image.open(BytesIO(ufile['body']))
        pixels = list(img.getdata())
        width, height = img.size
        pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
        np_img = np.array(pixels,dtype=np.uint8)
        raw_imgs.append(cv2.cvtColor(np_img, cv2.COLOR_BGR2RGB))
        probable =  RecognizeFace(raw_imgs) #["05c2caeeffa4850d6a774ee6fff54bb53f6f765a13fd666ea1ab987453332776"] #
        if probable != None:
            if len(probable) != 0 :
                digital_id = probable[0]
                state_addr = DigitalIDStateAddress.for_new_user(digital_id).address
                response = GetStateData(state_addr)
                if response['CanMarkAttendance'] == False:
                    self.write("ERR_NO_ATTENDANCE_PRIVILIDGE")
                    self.finish()
                    return
                else:
                    payload["action"] = "new_token"
                    payload['uname'] = response['Name']
                    token = hmac.new(os.urandom(32).hex().encode('utf-8'), digital_id.encode('utf-8'),hashlib.sha256).hexdigest()
                    payload['digital_id'] = digital_id
                    payload["access_token"] = token
                    tx_sawtooth = SawtoothClientStub(tf_name="digital_id",tf_version="1.1",payload=payload)
                    tx_sawtooth.set_address_scope(inputs=[state_addr],outputs=[state_addr])
                    tx_sawtooth.prepare_tx_batch()
                    response_x = tx_sawtooth.send()
                    entry = []
                    for org_id in response['Organizations']:
                        org_sa = OrgsStateAddress.for_new_org(org_id,"PADDING_TEXT_IGNORED").address
                        sa_data = GetStateData(org_sa)
                        entry.append((sa_data['Organization'],org_id))

                    self.write({
                        'AccessToken' : token,
                        'DigitalID' : digital_id,
                        'AppUsername' : payload['uname'],
                        'Organizations' : entry
                    })
                    self.finish()
                    return

        self.write("ERR_USER_NOT_RECOGNIZED")
        self.finish()
