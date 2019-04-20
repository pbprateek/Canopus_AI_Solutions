import numpy as np
import cv2
import os
import tensorflow as tf

json_file = open((os.getcwd() + '/DLPart' + '/face_recog_model.json'), 'r')
model_json = json_file.read()
json_file.close()


from keras.models import model_from_json
global graph,model
graph = tf.get_default_graph()
model = model_from_json(model_json)
model.load_weights((os.getcwd() + '/DLPart' + '/face_recog_model_weights.h5'))


def img_to_encoding(image_path):
    img1 = cv2.imread(image_path, 1)
    img1 = cv2.resize(img1, (96, 96)) 
    img = img1[...,::-1]
    img = np.around(np.transpose(img, (2,0,1))/255.0, decimals=12)
    x_train = np.array([img])
    with graph.as_default():
        embedding = model.predict_on_batch(x_train)
    return embedding




def verify_if_same(image_path_first,image_path_second):
    encoding_first = img_to_encoding(image_path_first)
    
    encoding_second = img_to_encoding(image_path_second)
    
    dist = np.linalg.norm(encoding_first-encoding_second)
    
    if dist<0.8:
        same_person = True
    else:
        same_person = False
        
    return same_person
 

#same = verify_if_same('andrew1.png','andrew2.png') 
#print(same)

#same = verify_if_same('sarukh2.jpg','sarukh3.jpg') 
#print(same)