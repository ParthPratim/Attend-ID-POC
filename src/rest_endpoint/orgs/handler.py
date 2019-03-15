import tornado.web
import tornado.escape
import json
import os
import hmac
import hashlib
from rest_endpoint.orgs.meta import frame_msg
from rest_endpoint.sawtooth_client.tx import SawtoothClientStub
from rest_endpoint.orgs.state import OrgsStateAddress

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
        rnd_org_id = hmac.new(os.urandom(16).hex().encode('utf-8'),(payload['org_name']+payload['creator_id']).encode('utf-8'),hashlib.sha256).hexdigest()
        payload["org_id"] = rnd_org_id
        sawtooth_rest_api =  SawtoothClientStub(tf_name="orgs",tf_version="1.0",payload=payload)
        address = OrgsStateAddress.for_new_org(payload['org_id'],payload['creator_id'])
        print(address.address)
        sawtooth_rest_api.set_address_scope(inputs=[address.address],outputs=[address.address])
        sawtooth_rest_api.prepare_tx_batch()
        response = sawtooth_rest_api.send()
        print(response)