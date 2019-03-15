import json
import hmac
import hashlib
import os
import tornado.web
from rest_endpoint.digital_id.meta import frame_msg
from rest_endpoint.digital_id.state import OrgsStateAddress
from rest_endpoint.sawtooth_client.tx import SawtoothClientStub

class DigitalIDHandler(tornado.web.RequestHandler):
    def post(self):
        payload = tornado.escape.json_decode(self.request.body)
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
        if "name" not in payload:
            self.write(json.dumps(
                frame_msg(
                    {
                        "msg" : "Username not given"
                    }
                )
                ,status="BAD_REQUEST"
            ))
            self.finish()
        digital_id = hmac.new(os.urandom(16).hex().encode('utf-8'),(payload['name']).encode('utf-8'),hashlib.sha256).hexdigest()
        payload["digital_id"] = digital_id
        state_addr = OrgsStateAddress.for_new_user(digital_id).address
        print(state_addr)
        tx_sawtooth = SawtoothClientStub(tf_name="digital_id",tf_version="1.0",payload=payload)
        tx_sawtooth.set_address_scope(inputs=[state_addr],outputs=[state_addr])
        tx_sawtooth.prepare_tx_batch()
        response = tx_sawtooth.send()