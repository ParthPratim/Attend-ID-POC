import csv
import cv2
import pickle
import json
import datetime
import numpy as np
from rest_endpoint.internals.ipfs_storage import IpfsStorage
from rest_endpoint.orgs.state import OrgsStateAddress
from rest_endpoint.digital_id.state import DigitalIDStateAddress
from rest_endpoint.internals.get_state_data import GetStateData
from bigchaindb.utils.bdb_ukey import Key
from bigchaindb.asset_logic.orgs import OrgsAssets
from fre_layer.train import TrainClassifier

PADDING_CSV = "event_sub/data/padding.csv"

def BuildOrgFRModel(org_id):
    address = OrgsStateAddress.for_new_org(org_id,"PADDING_TEXT_INGORED").address
    state_data = GetStateData(address)
    if state_data != False:
        keys = Key(state_data['BDB_pub_key'],state_data['BDB_priv_key'])
        m_list = OrgsAssets.GetOrgMemberList(keys)
        u_base = []
        with open(PADDING_CSV,"r") as train_csv:
            reader = csv.reader(train_csv)
            lines = list(reader)
            u_base = lines
        for member in m_list:
            did = member[1]
            u_sa = DigitalIDStateAddress.for_new_user(did).address
            sa_data = GetStateData(u_sa)
            if sa_data == False:
                return False
            else:
                t_hash = sa_data["TrainingImageHash"]
                u_base.append((did,t_hash))
        ct = 0
        persons = []
        imgs = []
        labels = []
        for entry in u_base:
            digital_id = entry[0]
            xhash = entry[1]
            persons.append(digital_id)
            rgbs = pickle.loads(IpfsStorage.from_hash(xhash).load_contents())['RGBS']
            print((len(rgbs)))
            for rgb in rgbs:
                imgs.append(rgb)
                labels.append(ct)
            ct = ct + 1

        tc =  TrainClassifier("facenet/20180402-114759/",
                              1000,
                              160,
                              "PIPE_OUT_MODEL",
                              imgs,
                              labels,
                              persons)
        picklable = tc.begin()
        ipfs = IpfsStorage()
        hash = ipfs.store_pyobj(picklable)
        return hash

    else:
        return False
