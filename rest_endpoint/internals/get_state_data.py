import urllib.request
import json
from urllib.error import HTTPError
import base64
import cbor

def fromRawData(data):
    return cbor.loads(data)

def GetStateData(addr):
    try:
        request = urllib.request.Request(
            'http://rest-api:8008/state/'+addr,
            method='GET')
        response = urllib.request.urlopen(request)
        js = json.loads(response.read().decode('utf-8'))
        if 'error' in js :
            return False
        return cbor.loads(base64.b64decode(js['data']))

    except HTTPError as e:
        return False

#GetStateData("f567055f847db48243c3016b6aec2ba5936755f25f2396b6bf0871d30462595e1df5a7")
