from fre_layer.readimg import load_images
from facenet import classifier
from facenet.utils import Args
import os

DATASET_DIR = 'test_dataset/train'
class TrainClassifier:
    def __init__(self,model,batch_size,image_size,classifier_filename,imgs,labels,persons):
        args = Args()
        args.mode = "TRAIN"
        args.model = model
        args.batch_size = batch_size
        args.image_size = image_size
        args.classifier_filename = classifier_filename
        args.imgs = imgs
        args.labels = labels
        args.class_names = persons
        self.args = args

    def begin(self):
        return classifier.main(self.args)

def x():
    imgs = []
    labels = []
    index = 0
    persons = sorted(os.listdir(DATASET_DIR))
    for person in persons:
        d_list = os.listdir(os.path.join(DATASET_DIR,person))
        imgs = imgs + load_images([os.path.join(DATASET_DIR,person,img_path) for img_path in d_list])
        labels = labels + [index for pic in d_list]
        index = index+1

    tc =  TrainClassifier("facenet/20180402-114759/",
                          1000,
                          160,
                          "facenet/20180402-114759/my_classifier.pkl",
                          imgs,
                          labels,
                          persons)
    tc.begin()
