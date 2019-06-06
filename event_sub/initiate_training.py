import csv
import cv2
import pickle
import json
import datetime
import numpy as np
from rest_endpoint.internals.ipfs_storage import IpfsStorage
from fre_layer.train import TrainClassifier

TRAIN_CSV = "event_sub/data/train.csv"
LOG_FILE = "event_sub/data/train.json"

def Now(new_digital_id,hash):

    with open(TRAIN_CSV,"a") as train_csv:
        writer = csv.writer(train_csv)
        writer.writerow([new_digital_id,hash])

    train_csv.close()

    with open(TRAIN_CSV,"r") as train_csv:
        reader = csv.reader(train_csv)
        lines = list(reader)
        imgs = []
        labels = []
        ct = 0
        persons = []
        if len(lines) == 1 :
            return
        for entry in lines:
            digital_id = entry[0]
            xhash = entry[1]
            append = 0
            persons.append(digital_id)
            rgbs = pickle.loads(IpfsStorage.from_hash(xhash).load_contents())['RGBS']
            print((len(rgbs)))
            for rgb in rgbs:
                imgs.append(rgb)
                labels.append(ct)
            ct = ct + 1
        print((np.array(imgs).shape))
        print((np.array(labels).shape))
        tc =  TrainClassifier("facenet/20180402-114759/",
                              1000,
                              160,
                              "facenet/20180402-114759/test-classifier.pkl",
                              imgs,
                              labels,
                              persons)
        tc.begin()
        logs = {}
        with open(LOG_FILE,"r") as log:
            logs = json.load(log)
            logs['Last-Updated'] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        with open(LOG_FILE,"w") as log:
            json.dump(logs,log)


    train_csv.close()
