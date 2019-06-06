import cv2
import numpy
import requests

def RecognizeFace(rgbs):
    identify = "http://172.30.0.1:7071/api/IdentifyFace"
    request = {}
    img_index = 1
    for rgb in rgbs:
        img_bytes = numpy.array(cv2.imencode('.jpg', rgb)[1]).tostring()
        img_hex = img_bytes.hex()
        request['img'+str(img_index)] = img_hex
        img_index = img_index + 1

    response =  requests.post(identify,json=request)
    print(response.content.decode())
    digital_id = response.json()['identified']
    if len(digital_id) == 0:
        return None
    else:
        return digital_id
