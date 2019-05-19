import numpy as np
import cv2
import dlib
import os
import sys
from imutils import face_utils
import math

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,15)
fontScale              = 0.5
fontColor              = (0,0,0)
lineType               = 2

protoFile = "pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
weightsFile = "pose/mpi/pose_iter_160000.caffemodel"

base_dir = "../fre_layer/models/"
modelFile = base_dir+"opencv_face_detector_uint8.pb"
configFile = base_dir+"opencv_face_detector.pbtxt"
face_cascade = cv2.CascadeClassifier(base_dir+'haarcascade_frontalface_default.xml')
net2 = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def RecordVideo():

    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Attend-ID : Image Dataset Generating Tool",cv2.WINDOW_GUI_EXPANDED)
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH);
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT);
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4',fourcc, 15.0, (int(w),int(h)))

    if cap.isOpened(): # try to get the first frame
        rval, frame = cap.read()
    else:
        rval = False
    while rval:
        cv2.imshow('Attend-ID : Image Dataset Generating Tool', frame)
        if rval:
            out.write(frame)
        else:
            break

        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break
        rval, frame = cap.read()

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def ImageSnap(uname):
    interesting_frames = []
    previous_nose_tip = [-1,-1]
    curr_frame_index = 0
    prev_gap_x = 30
    prev_gap_y = 30


    vc = cv2.VideoCapture('output.mp4')
    frames_len = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))

    print("Processing " + str(frames_len) + " frames...")
    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        # Read image
        im = frame
        print(bcolors.OKBLUE+" Working on Frame no : " + str(curr_frame_index + 1) + "/" + str(frames_len))
        sys.stdout.write("\033[F") # Cursor up one line
        (h, w) = im.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(im, (300,300)), 1.0, (300, 300), (103.93, 116.77, 123.68))
        net2.setInput(blob)
        detections = net2.forward()
        max = 0
        ind = -1
        for i in range(0,detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5 and confidence > max:
                ind = i
                max = confidence
        if ind != -1:
            x1 = int(detections[0, 0, ind, 3] * w)
            y1 = int(detections[0, 0, ind, 4] * h)
            x2 = int(detections[0, 0, ind, 5] * w)
            y2 = int(detections[0, 0, ind, 6] * h)


            predictor = dlib.shape_predictor("../fre_layer/models/shape_predictor_68_face_landmarks.dat")
            rect = dlib.rectangle(x1,y1,x2,y2)
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            image_points = np.array([
                (shape[33][0],shape[33][1])
            ])

            size = im.shape


            if previous_nose_tip[0] == previous_nose_tip[1] == -1:
                previous_nose_tip = image_points[0] # Set default nose tip
            else:

                dx = abs(image_points[0][0] - previous_nose_tip[0])
                dy = abs(image_points[0][1] - previous_nose_tip[1])


                if dx >= prev_gap_x:
                    # Significant head rotation in X space
                    interesting_frames.append(curr_frame_index)
                    previous_nose_tip = image_points[0] # Set default nose tip
                    prev_gap_x = 10

                elif dy >= prev_gap_y:
                    # Significant head rotation In Y space
                    interesting_frames.append(curr_frame_index)
                    previous_nose_tip = image_points[0] # Set default nose tip
                    prev_gap_y = 10

        curr_frame_index  = curr_frame_index+1
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break



    for i in range(0,len(interesting_frames),4):
        vc.set(1, interesting_frames[i])
        res, frame = vc.read()
        cv2.imwrite(os.path.join(uname,"training_img_"+str(i)+".jpg"),frame)
    vc.release()



if __name__ == "__main__":
    print(bcolors.HEADER + "Welcome to AttendID Image Dataset generator")
    print("\n")
    print(bcolors.BOLD + "Enter Name (any) : ")
    name = input()
    if os.path.isdir(name):
        os.rmdir(name)

    os.mkdir(name)
    print(bcolors.WARNING + bcolors.BOLD + bcolors.UNDERLINE + "Move your face slowly to the left, right, up and down !!" + bcolors.ENDC)
    RecordVideo()
    ImageSnap(name)
