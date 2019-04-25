from google_images_download import google_images_download
from keras import models
from keras import layers
from keras.applications import MobileNetV2
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
from keras import backend as K
import matplotlib.pyplot as plt


def downloadImages(keywords, folder_name):
    response = google_images_download.googleimagesdownload()  # class instantiation
    #TODO change limit to 80 for final Demo
    arguments = {"keywords": keywords, "limit": 4,
                 "output_directory": "DLPart/ImageClassifierJunk/" + folder_name}  # creating list of arguments
    response.download(arguments)  # passing the arguments to the function


def defineModel(folder_name):
    K.clear_session()
    global graph, model
    train_dir = "DLPart/ImageClassifierJunk/" + folder_name

    conv_base = MobileNetV2(weights='imagenet', include_top=False, input_shape=(128, 128, 3))
    conv_base.trainable = False
    model = models.Sequential()
    model.add(conv_base)
    model.add(layers.Flatten())
    model.add(layers.Dense(512, activation='relu'))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(2, activation='softmax'))

    train_datagen = ImageDataGenerator(rescale=1. / 255, rotation_range=40, width_shift_range=0.2,
                                       height_shift_range=0.2, shear_range=0.2, zoom_range=0.2, horizontal_flip=True,
                                       fill_mode='nearest')
    train_generator = train_datagen.flow_from_directory(train_dir, target_size=(128, 128), batch_size=20)

    model.compile(loss='categorical_crossentropy', optimizer=optimizers.RMSprop(lr=2e-5), metrics=['acc'])
    graph = tf.get_default_graph()
    with graph.as_default():
        history1 = model.fit_generator(train_generator, steps_per_epoch=4, epochs=5)

        for layer in conv_base.layers:
            if layer.name in ['block_16_project', 'block_16_project_BN', 'Conv_1', 'Conv_1_bn', 'out_relu']:
                layer.trainable = True
            else:
                layer.trainable = False
        model.compile(loss='categorical_crossentropy', optimizer=optimizers.RMSprop(lr=1e-5), metrics=['acc'])

        history2 = model.fit_generator(train_generator, steps_per_epoch=4, epochs=5)

        loss = list()
        loss.extend(history1.history['loss'])
        loss.extend(history2.history['loss'])
        accuracy = history2.history['acc'][-1]
        plt.plot(loss)
        plt.title('Model loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        model.save('weights.h5')
        plt.savefig('image/static/image/images/graph.png')

        '''
        Our Default folder is Canopus_AI_Solution so above model and image will get saved in that folder(refering 
        to line no 63 and 64).If u want them to be saved in image/static then change above lines to:
        model.save('image/static/%s.h5' % folder_name)
        plt.savefig('image/static/%s.png'%folder_name)
        and the name will be query1 + query2,
        so if u search for human and car then the filename will become humancar.h5 and humancar.png 
        so use them accordingly to display image and provide download link after training is done.
        '''
        return accuracy


def train_weights_Image_classifier(query1, query2):
    keywords = query1 + "," + query2
    foldername = query1 + query2
    downloadImages(keywords, foldername)
    defineModel(foldername)




