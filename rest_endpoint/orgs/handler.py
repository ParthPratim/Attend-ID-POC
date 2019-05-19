import tornado.web
import tornado.escape
import json
import os
import hmac
import hashlib
import cv2
import numpy as np
from PIL import Image
from OpenSSL import crypto
from tornado import httpclient
from rest_endpoint.orgs.meta import frame_msg
from rest_endpoint.sawtooth_client.tx import SawtoothClientStub
from rest_endpoint.orgs.state import OrgsStateAddress
from rest_endpoint.digital_id.state import DigitalIDStateAddress
from rest_endpoint.internals.get_state_data import GetStateData
from rest_endpoint.internals.ssl_auth import *
from rest_endpoint.internals.ipfs_storage import IpfsStorage
from rest_endpoint.orgs.build_fr import BuildOrgFRModel
from bigchaindb.asset_logic.orgs import OrgsAssets
from bigchaindb.utils.bdb_ukey import Key
from bigchaindb.utils.bdb_ukey import GenerateRandomKeyPair
from facenet.face_recognition_image import RecognizeFace

ACTION_CREATE_NEW_ORG = "CREATE_NEW_ORG"
ACTION_ADD_NEW_ORG_MEMBER = "ADD_NEW_ORG_MEMBER"
ACTION_TRANSFER_ORG_MEMBER = "TRANSFER_ORG_MEMBER"
ACTION_BUILD_FR_MODEL = "BUILD_FR_MODEL"
SERVER_PK12_FILE_HASH = "QmQEjF8i8iPT7bdM8u1ncJhWXBdThYDF3Dj98ocLzJdX6q"


class OrgsHandler(tornado.web.RequestHandler):
    def post(self):
        payload = tornado.escape.json_decode(self.request.body)
        if "action" not in payload :
            self.write(json.dumps(
                frame_msg({
                    "msg" : "Action type missing",
                },status="BAD_REQUEST")
            ))
            self.finish()
        elif "org_name" not in payload :
            self.write(json.dumps(
                frame_msg({
                    "msg" : "Organization name missing",
                },status="BAD_REQUEST")
            ))
            self.finish()
        elif "creator_id" not in payload :
            self.write(json.dumps(
                frame_msg({
                    "msg" : "Creator's DigitalID missing",
                },status="BAD_REQUEST")
            ))
            self.finish()

        if "org_id" not in payload:
            rnd_org_id = hmac.new(os.urandom(16).hex().encode('utf-8'),(payload['org_name']+payload['creator_id']).encode('utf-8'),hashlib.sha256).hexdigest()
            payload["org_id"] = rnd_org_id


        process = True
        address = OrgsStateAddress.for_new_org(payload['org_id'],payload['creator_id'])
        inputs=[address.address]
        outputs=[address.address]
        if payload['action'] == ACTION_CREATE_NEW_ORG:
            ipfs = IpfsStorage()
            hash = ipfs.from_hash(SERVER_PK12_FILE_HASH)
            server_p12 = crypto.load_pkcs12(hash.load_contents())

            server = {
                "cert" : server_p12.get_certificate(),
                "key" : server_p12.get_privatekey()
            }

            client = CreateUserCertAndKey(payload['org_id'])
            cert = create_cert(client["cert"],server['key'])
            pk = crypto.PKCS12()
            pk.set_certificate(cert)
            pk.set_privatekey(client['key'])
            pk12_cert = pk.export()
            hash = ipfs.store_bytes(pk12_cert)
            payload['certificate_hash'] = hash
            k_p = GenerateRandomKeyPair.create()
            payload['bdb_pub_key'] = k_p['pub_key']
            payload['bdb_priv_key'] = k_p['priv_key']

        if payload['action'] == ACTION_ADD_NEW_ORG_MEMBER:

            # ADD A NEW MEMBER ON bigchaindb
            digital_id_creator_state_addr = DigitalIDStateAddress.for_new_user(payload['creator_id']).address
            digital_id_newm_state_addr = DigitalIDStateAddress.for_new_user(payload['new_member_id']).address
            org_addr = OrgsStateAddress.for_new_org(payload['org_id'],payload['creator_id']).address
            did_data1 = GetStateData(digital_id_creator_state_addr)
            did_data2 = GetStateData(digital_id_newm_state_addr)
            did_data3 = GetStateData(org_addr)
            print("CREATOR : "+digital_id_creator_state_addr)
            print("MEMBER : "+digital_id_newm_state_addr)
            print(did_data1)
            print(did_data2)
            if did_data1 != False and did_data2 != False:
                u_keys = Key(did_data3['BDB_pub_key'],did_data3['BDB_priv_key'])
                status = OrgsAssets.NewMember(payload['new_member_id'],u_keys)
                print(status)
                if status == False:
                    process = status
                else:
                    inputs.append(digital_id_newm_state_addr)
                    outputs.append(digital_id_newm_state_addr)
            else:
                print("FALSE")
        if payload['action'] == ACTION_TRANSFER_ORG_MEMBER :
            digital_id_creator_state_addr = DigitalIDStateAddress.for_new_user(payload['creator_id']).address
            digital_id_currm_state_addr = DigitalIDStateAddress.for_new_user(payload['curr_member_id']).address
            digital_id_neworg_state_addr = DigitalIDStateAddress.for_new_user(payload['new_org_creator']).address
            org_addr = OrgsStateAddress.for_new_org(payload['org_id'],payload['creator_id']).address
            new_org_addr = OrgsStateAddress.for_new_org(payload['new_org_id'],payload['new_org_creator']).address
            did_data1 = GetStateData(digital_id_creator_state_addr)
            did_data2 = GetStateData(digital_id_currm_state_addr)
            did_data3 = GetStateData(digital_id_neworg_state_addr)
            did_data4 = GetStateData(org_addr)
            did_data5 = GetStateData(new_org_addr)
            if did_data1 != False and did_data2 != False and did_data3 != False:
                u_keys = Key(did_data4['BDB_pub_key'],did_data4['BDB_priv_key'])
                asset_id = OrgsAssets.GetAssetID(payload['curr_member_id'],u_keys)
                if asset_id == False:
                    print("Failed Loading asset...")
                else:
                    print(asset_id)
                    print(u_keys.public_key)
                    new_keys = Key(did_data5['BDB_pub_key'],did_data5['BDB_priv_key'])
                    status = OrgsAssets.TransferMember(asset_id,u_keys,new_keys)
                    if status == False:
                        process = status
                    else:
                        inputs.append(new_org_addr)
                        outputs.append(new_org_addr)
                        inputs.append(digital_id_currm_state_addr)
                        outputs.append(digital_id_currm_state_addr)
            else:
                print("Invalid Digital IDs given")
        if payload['action'] == ACTION_BUILD_FR_MODEL:
            response = BuildOrgFRModel(payload['org_id'])
            if response == False:
                self.write({
                    'Status' : 0
                })
                self.finish()
                return
            else:
                payload['frmodel'] = response

        if process:
            print(payload)
            sawtooth_rest_api =  SawtoothClientStub(tf_name="orgs",tf_version="1.9",payload=payload)
            print(address.address)
            sawtooth_rest_api.set_address_scope(inputs=inputs,outputs=outputs)
            sawtooth_rest_api.prepare_tx_batch()
            response = sawtooth_rest_api.send()

            if payload['action'] == ACTION_CREATE_NEW_ORG:
                file_name = payload['org_name']+"."+payload['org_id']+".p12"
                self.write({
                    "Headers" : {
                        "Content-Disposition" : "attachment; filename=\""+file_name+"\""
                        },
                    "Response" : pk12_cert.hex()
                    })
                self.finish()
            else:
                self.write(
                    {
                        "Status" : 1
                    }
                )
                self.finish()

        else:
            print("Stopped processing request...")

class OrgInfo(tornado.web.RequestHandler):
    def get(self):
        payload = tornado.escape.json_decode(self.request.body)
        if payload['action'] == "GET_ORG_MEMBERS":
            org_addr = OrgsStateAddress.for_new_org(payload['org_id'],"SOME_BLUFF_TEXT").address
            org_data = GetStateData(org_addr)
            print(org_data)
            k = Key(org_data['BDB_pub_key'],org_data['BDB_priv_key'])
            m_list = OrgsAssets.GetOrgMemberList(k)
            self.write({
                "Members" : m_list
            })
            self.finish()
