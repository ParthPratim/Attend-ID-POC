import os
import ipfshttpclient
import hmac
import hashlib
import csv
import json
import numpy as np
from PIL import Image


conn = ipfshttpclient.connect(host="ipfs-net")

struct_newuser = {
    "DigitalID" : "",
    "RGBS" : []
}

TRAIN_CSV = "../event_sub/data/train.csv"
PADDING_CSV = "../event_sub/data/padding.csv"
SERVER_P12 = "../keys/ssl/server.p12"

for persons in os.listdir("../test_dataset/train"):
    raw_imgs = []
    for ufile in os.listdir("../test_dataset/train/"+persons):
        img = Image.open(os.path.join("../test_dataset/train",persons,ufile))
        pixels = list(img.getdata())
        width, height = img.size
        pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
        np_img = np.array(pixels,dtype=np.uint8)
        raw_imgs.append(np_img)

    digital_id = hmac.new(os.urandom(16).hex().encode('utf-8'),(persons).encode('utf-8'),hashlib.sha256).hexdigest()
    struct_newuser["DigitalID"] = digital_id
    struct_newuser["RGBS"] = raw_imgs
    hash = conn.add_pyobj(struct_newuser)

    with open(TRAIN_CSV,"a") as train_csv:
        writer = csv.writer(train_csv)
        writer.writerow([digital_id,hash])

    with open(PADDING_CSV,"a") as train_csv:
        writer = csv.writer(train_csv)
        writer.writerow([digital_id,hash])

hash = conn.add(SERVER_P12)
with open("../config.json","r") as cjf:
    cj = json.load(cjf)
    cj["SERVER_PK12_FILE_HASH"] = hash['Hash']

with open("../config.json","w") as cjf:
    json.dump(cj,cjf)

print("Initial Setup Has Been Done !")
