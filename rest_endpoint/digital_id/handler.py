import json
import hmac
import hashlib
import os
import tornado.web
import pickle
import time
import numpy as np
import cv2
import uuid
import mimetypes
from OpenSSL import crypto
from PIL import Image
from io import BytesIO
from functools import partial
from tornado.web import HTTPError
from rest_endpoint.digital_id.meta import frame_msg
from rest_endpoint.digital_id.state import DigitalIDStateAddress
from rest_endpoint.sawtooth_client.tx import SawtoothClientStub
from rest_endpoint.internals.ssl_auth import *
from rest_endpoint.internals.ipfs_storage import IpfsStorage
from rest_endpoint.internals.get_state_data import GetStateData
from bigchaindb.utils.bdb_ukey import GenerateRandomKeyPair
from fre_layer.finalize_image import DetectAlignResize
from fre_layer.readimg import raw_process
from facenet.face_recognition_image import RecognizeFace


SERVER_PK12_FILE_HASH = "QmQEjF8i8iPT7bdM8u1ncJhWXBdThYDF3Dj98ocLzJdX6q"

class DigitalIDHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def post(self):
        payload = { }

        files = self.request.files['images']

        payload['action'] = self.get_body_argument("action", default=None, strip=False)
        payload['uname'] = self.get_body_argument("uname", default=None, strip=False)
        payload['cn'] = self.get_body_argument("cn", default=None, strip=False)

        if "action" not in payload:
            self.write(json.dumps(
                frame_msg(
                    {
                        "msg" : "Action not specified"
                    }
                ),
                status="BAD_REQUEST"
            ))
            self.finish()
        if "uname" not in payload:
            self.write(json.dumps(
                frame_msg(
                    {
                        "msg" : "Username not given"
                    }
                )
                ,status="BAD_REQUEST"
            ))
            self.finish()

        digital_id = hmac.new(os.urandom(16).hex().encode('utf-8'),(payload['uname']).encode('utf-8'),hashlib.sha256).hexdigest()
        keypair = GenerateRandomKeyPair.create()
        payload["digital_id"] = digital_id
        payload["bdb_pub_key"] = keypair['pub_key']
        payload["bdb_priv_key"] = keypair['priv_key']
        state_addr = DigitalIDStateAddress.for_new_user(digital_id).address
        print(state_addr)

        struct_newuser = {
            "DigitalID" : digital_id,
            "RGBS" : []
        }
        ipfs = IpfsStorage()

        np_imgs = []
        raw_imgs = []
        for ufile in files:
            img = Image.open(BytesIO(ufile['body']))
            pixels = list(img.getdata())
            width, height = img.size
            pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
            np_img = np.array(pixels,dtype=np.uint8)
            raw_imgs.append(cv2.cvtColor(np_img, cv2.COLOR_BGR2RGB))
            if len(np_img.shape) > 2 and np_img.shape[2] == 4:
                np_img = cv2.cvtColor(np_img, cv2.COLOR_BGRA2BGR)
            np_imgs.append(np_img)

            print(ufile['filename'])

        probable = RecognizeFace(raw_imgs)
        if probable != None:
            if len(probable) != 0 :
                print("PROBABLY : " + probable[0])
                self.write({
                    "Headers" : {
                        "Content-Type" : "application/json"
                        },
                    "DigitalID" : probable[0],
                    "Response" : ("This user is registered with Digital-ID  : "+probable[0]+". Stop faking and try again WITHOUT SPOOFINNG.").encode().hex()
                    })
                self.finish()
                return

        for np_img in np_imgs:
            final_img = np.array(DetectAlignResize(np_img).process())
            if final_img is not None and len(final_img.shape)  != 0:
                print("ADDED")
                final_img = raw_process(final_img)
                struct_newuser['RGBS'].append(final_img)

        struct_newuser['RGBS'] =  np.array(struct_newuser['RGBS'])
        snu_hash = ipfs.store_pyobj(struct_newuser)
        payload['training_image_hash'] = snu_hash



        hash = ipfs.from_hash(SERVER_PK12_FILE_HASH)
        server_p12 = crypto.load_pkcs12(hash.load_contents())

        server = {
            "cert" : server_p12.get_certificate(),
            "key" : server_p12.get_privatekey()
        }

        client = CreateUserCertAndKey(digital_id)
        cert = create_cert(client["cert"],server['key'])
        pk = crypto.PKCS12()
        pk.set_certificate(cert)
        pk.set_privatekey(client['key'])
        pk12_cert = pk.export()
        hash = ipfs.store_bytes(pk12_cert)
        payload['certificate_hash'] = hash



        tx_sawtooth = SawtoothClientStub(tf_name="digital_id",tf_version="1.1",payload=payload)
        tx_sawtooth.set_address_scope(inputs=[state_addr],outputs=[state_addr])
        tx_sawtooth.prepare_tx_batch()
        response = tx_sawtooth.send()
        print(payload["uname"] + "  :  " + digital_id)
        file_name = payload["uname"]+"."+digital_id+".p12"

        if payload['action'] == "create":
            while(GetStateData(state_addr) == False):
                time.sleep(0.8)

        self.write({
            "Headers" : {
                "Content-Disposition" : "attachment; filename=\""+file_name+"\""
            },
            "DigitalID" : digital_id,
            "Response" : pk12_cert.hex()
        })
        self.finish()
        return
