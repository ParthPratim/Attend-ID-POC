from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pickle
import sys
import time
import operator
import cv2
import numpy as np
import tensorflow as tf
from scipy import misc
from facenet import facenet
from facenet.align import detect_face
from scipy import misc
from facenet.facenet import to_rgb , prewhiten, crop, flip

def load_image(img):
    image_size = 160
    img = prewhiten(img)
    return img


modeldir = 'facenet/20180402-114759/'
classifier_filename = 'facenet/20180402-114759/test-classifier.pkl'
npy=''


def RecognizeFace(frames,model=None,class_names=None):

    with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with sess.as_default():
            pnet, rnet, onet = detect_face.create_mtcnn(sess, npy)

            minsize = 20  # minimum size of face
            threshold = [0.6, 0.7, 0.7]  # three steps's threshold
            factor = 0.709  # scale factor
            margin = 32
            frame_interval = 3
            batch_size = 1000
            image_size = 160
            input_image_size = 160

            print('Loading feature extraction model')
            facenet.load_model(modeldir)

            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
            embedding_size = embeddings.get_shape()[1]


            classifier_filename_exp = os.path.expanduser(classifier_filename)
            if model == None or class_names == None:
                with open(classifier_filename_exp, 'rb') as infile:
                    (model, class_names) = pickle.load(infile)

            # video_capture = cv2.VideoCapture("akshay_mov.mp4")
            c = 0

            HumanNames = class_names
            print(HumanNames)

            print('Start Recognition!')
            prevTime = 0
            # ret, frame = video_capture.read()
            #frame = cv2.imread(img_path,0)

            #frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)    #resize frame (optional)
            total_faces_detected = {}
            for frame in frames:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                curTime = time.time()+1    # calc fps
                timeF = frame_interval

                if (c % timeF == 0):
                    find_results = []

                    if frame.ndim == 2:
                        frame = facenet.to_rgb(frame)
                        frame = frame[:, :, 0:3]
                        bounding_boxes, _ = detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)
                        nrof_faces = bounding_boxes.shape[0]
                        print('Face Detected: %d' % nrof_faces)

                        if nrof_faces > 0:
                            det = bounding_boxes[:, 0:4]
                            img_size = np.asarray(frame.shape)[0:2]

                            cropped = []
                            scaled = []
                            scaled_reshape = []
                            bb = np.zeros((nrof_faces,4), dtype=np.int32)

                            for i in range(nrof_faces):
                                emb_array = np.zeros((1, embedding_size))

                                bb[i][0] = det[i][0]
                                bb[i][1] = det[i][1]
                                bb[i][2] = det[i][2]
                                bb[i][3] = det[i][3]

                                #inner exception
                                if bb[i][0] <= 0 or bb[i][1] <= 0 or bb[i][2] >= len(frame[0]) or bb[i][3] >= len(frame):
                                    print('face is too close')
                                    break

                                cropped.append(frame[bb[i][1]:bb[i][3], bb[i][0]:bb[i][2], :])
                                cropped[i] = facenet.flip(cropped[i], False)
                                scaled.append(misc.imresize(cropped[i], (image_size, image_size), interp='bilinear'))
                                scaled[i] = cv2.resize(scaled[i], (input_image_size,input_image_size), interpolation=cv2.INTER_CUBIC)
                                scaled[i] = facenet.prewhiten(scaled[i])
                                scaled_reshape.append(scaled[i].reshape(-1,input_image_size,input_image_size,3))
                                feed_dict = {images_placeholder: scaled_reshape[i], phase_train_placeholder: False}
                                emb_array[0, :] = sess.run(embeddings, feed_dict=feed_dict)

                                predictions = model.predict_proba(emb_array)
                                print(predictions)
                                best_class_indices = np.argmax(predictions, axis=1)
                                # print(best_class_indices)
                                best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]

                                #plot result idx under box
                                text_x = bb[i][0]
                                text_y = bb[i][3] + 20
                                print('Result Indices: ', best_class_indices[0])
                                print(HumanNames)
                                for H_i in HumanNames:
                                    # print(H_i)
                                    if HumanNames[best_class_indices[0]] == H_i and best_class_probabilities >= 0.4:
                                        result_names = HumanNames[best_class_indices[0]]
                                        if result_names in total_faces_detected:
                                            if predictions[0][best_class_indices[0]] > total_faces_detected[result_names]:
                                                total_faces_detected[result_names] = predictions[0][best_class_indices[0]]
                                        else:
                                            total_faces_detected[result_names] = predictions[0][best_class_indices[0]]

                    else:
                        print("BHAKKK")
            if len(total_faces_detected) == 0 :
                return None
            else:
                x = sorted(total_faces_detected.items(), key=operator.itemgetter(1))
                return [x[len(x)-1][0]]
#RGB = []
#for img in os.listdir('../novel-data/val'):
#    RGB.append(cv2.imread("../novel-data/val/"+img))

#RGB.append(cv2.imread("facenet/t2.jpg"))
#RGB.append(cv2.imread("facenet/t5.jpg"))
#RGB.append(cv2.imread("facenet/test.PNG"))
#print(RecognizeFace(RGB))
