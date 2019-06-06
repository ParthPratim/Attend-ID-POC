import cv2
import os
import numpy as np
import dlib
from imutils import face_utils

base_dir = "fre_layer/models/"
modelFile = base_dir+"opencv_face_detector_uint8.pb"
configFile = base_dir+"opencv_face_detector.pbtxt"
net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

class DetectAlignResize:
    def __init__(self,img):
        self._img_to_process = img

    def process(self):
        return self.align_reshape_face(self.detect_faces())

    def detect_faces(self):
        img =  self._img_to_process
        print((img.shape))
        (h, w) = img.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (300,300)), 1.0, (300, 300), (103.93, 116.77, 123.68))
        net.setInput(blob)
        detections = net.forward()
        max = 0
        ind = -1
        for i in range(0,detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.4 and confidence > max:
                ind = i
                max = confidence
        if ind != -1:
            x1 = int(detections[0, 0, ind, 3] * w)
            y1 = int(detections[0, 0, ind, 4] * h)
            x2 = int(detections[0, 0, ind, 5] * w)
            y2 = int(detections[0, 0, ind, 6] * h)

            predictor = dlib.shape_predictor(base_dir+"shape_predictor_5_face_landmarks.dat")
            rect = dlib.rectangle(x1,y1,x2,y2)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            print(shape)
            return [{
                'box' : [x1,y1,x2,y2],
                'keypoints' : {
                    'left_eye' : ( int((shape[0][0]+shape[1][0])/2) , int((shape[0][1]+shape[1][1])/2) ),
                    'right_eye' : ( int((shape[2][0]+shape[3][0])/2) , int((shape[2][1]+shape[3][1])/2) )
                    }
                }]
        else:
            cv2.imwrite("problem.jpg",img)

        return None

    def align_reshape_face(self,d):
        if d is None:
            return None
        img = self._img_to_process
        bbox = d[0]['box']
        keypoints = d[0]['keypoints']
        dY = keypoints['right_eye'][1] - keypoints['left_eye'][1]
        dX = keypoints['right_eye'][0] - keypoints['left_eye'][0]
        angle = np.degrees(np.arctan2(dY, dX)) - 180
        img = DetectAlignResize.rotate_by_angle(img,angle)
        return img

    @staticmethod
    def rotate_by_angle(in_img,angle):
        image_center = tuple(np.array(in_img.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(in_img, rot_mat, in_img.shape[1::-1], flags=cv2.INTER_LINEAR)
        return np.array(result)

    @staticmethod
    def resize(in_img,size):
        v = in_img[:]
        size = (int(size[0]),int(size[1]))
        return cv2.resize(v,size, interpolation = cv2.INTER_AREA)

    @staticmethod
    def crop(in_img,size,cords=(0,0)):
        v = in_img[:]
        return np.array(v[cords[1]:size[1],cords[0]:size[0]],dtype=np.uint8)
