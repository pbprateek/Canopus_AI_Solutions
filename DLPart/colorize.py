from keras.models import load_model
from skimage.color import rgb2lab, lab2rgb, rgb2gray, gray2rgb
from skimage.transform import resize
from skimage.io import imsave
import numpy as np
import os
import random
import tensorflow as tf
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.applications.inception_resnet_v2 import preprocess_input
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img





def create_inception_embedding(grayscaled_rgb):
    inception = InceptionResNetV2(weights='imagenet', include_top=True)
    inception.graph = tf.get_default_graph()
    grayscaled_rgb_resized = []
    for i in grayscaled_rgb:
        i = resize(i, (299, 299, 3), mode='constant')
        grayscaled_rgb_resized.append(i)
    grayscaled_rgb_resized = np.array(grayscaled_rgb_resized)
    grayscaled_rgb_resized = preprocess_input(grayscaled_rgb_resized)
    with inception.graph.as_default():
        embed = inception.predict(grayscaled_rgb_resized)
    return embed






def colorme(path_to_image,image_name):
    model = load_model('DLPart/try1.h5')
    inception = InceptionResNetV2(weights='imagenet', include_top=True)
    inception.graph = tf.get_default_graph()


    color_me = []
    color_me.append(img_to_array(load_img(path_to_image)))

    color_me = np.array(color_me, dtype=float)
    gray_me = gray2rgb(rgb2gray(1.0/255*color_me))
    color_me_embed = create_inception_embedding(gray_me)
    color_me = rgb2lab(1.0/255*color_me)[:,:,:,0]
    color_me = color_me.reshape(color_me.shape+(1,))

    output = model.predict([color_me, color_me_embed])
    output = output * 128

    for i in range(len(output)):
        cur = np.zeros((256, 256, 3))
        cur[:,:,0] = color_me[i][:,:,0]
        cur[:,:,1:] = output[i]
        imsave('image/static/image/images'+image_name+".png", lab2rgb(cur))

colorme('DLPart/kid.jpg','kidc')