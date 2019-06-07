import cv2
import pickle
import numpy
import requests
import logging
from rest_endpoint.internals.ipfs_storage import IpfsStorage

class AzureFaceModule:

    @staticmethod
    def AddNewPerson(digital_id):
        new_person = "https://frelayerattendid.azurewebsites.net/api/createnewperson?code=4rsj0yDyPSIukboTd3EygoNKfFyrG7h6ONUh9fPKdgld1tc7xo7/zA=="
        response =  requests.post(new_person,json={'digital_id':digital_id}).json()
        if "error" in response :
            logging.info("Failed to add Digital_ID to Azure Face Cognitive Engine !")
            return False
        else:
            return response['personId']

    @staticmethod
    def AddFace(rgbs,person_id):
        add_face = "https://frelayerattendid.azurewebsites.net/api/addpersonface?code=NJiVHe5NHvhVff4Kuvht2AEiuomWBJ9QWjgpTmaH2Kto1Fln8WtkgA=="
        request = {
            'person_id':person_id,
            }

        img_index = 1
        for rgb in rgbs:
            face_bytes = numpy.array(cv2.imencode('.jpg', rgb)[1]).tostring()
            f_hex = face_bytes.hex()
            request['tr_img'+str(img_index)] = f_hex
            img_index = img_index + 1

        response = requests.post(add_face,json=request).json()
        logging.info("Added " + str(response['facesAdded']) + " / " + str(len(rgbs)) + " faces !")
        return response['facesAdded']

    @staticmethod
    def NowTrain():
         train = "https://frelayerattendid.azurewebsites.net/api/trainmodel?code=T9DPkbs8z5F8b8SZ4pQLy1IVEgFJ2YWlaXtGBDfMVB7mingOz3mTbA=="
         #requests.post(train,json={"action":"train"})

    @staticmethod
    def initiate_cloud_training(digital_id,hash):
        rgbs = pickle.loads(IpfsStorage.from_hash(hash).load_contents())['RGBS']
        for rgb in rgbs:
            person_id = AzureFaceModule.AddNewPerson(digital_id)
            faces_added = AzureFaceModule.AddFace(rgbs,person_id)
            if faces_added > 0 :
                AzureFaceModule.NowTrain()
                logging.info("Initiated Training on the Azure Cloud....")
