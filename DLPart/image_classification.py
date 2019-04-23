from google_images_download import google_images_download
from keras import models
from keras import layers
from keras.applications import MobileNetV2
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator


query1 = 'chair'
query2 = 'beds'


def downloadImages(keywords):
    response = google_images_download.googleimagesdownload()  # class instantiation
    arguments = {"keywords": keywords, "limit": 80,
                 "output_directory": "ImageClassifierJunk/"+query1+query2}  # creating list of arguments
    response.download(arguments)  # passing the arguments to the function


def defineModel():
    train_dir = "DLPart/ImageClassifierJunk/"+query1+query2

    conv_base = MobileNetV2(weights='imagenet', include_top=False,input_shape = (128, 128,3))
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
    train_generator = train_datagen.flow_from_directory(train_dir, target_size=(128, 128), batch_size=64)

    model.compile(loss='categorical_crossentropy', optimizer=optimizers.RMSprop(lr=2e-5), metrics=['acc'])
    history = model.fit_generator(train_generator, steps_per_epoch=3, epochs=5)

    for layer in conv_base.layers:
        if layer.name in ['block_16_project','block_16_project_BN','Conv_1','Conv_1_bn','out_relu']:
            layer.trainable = True
        else:
            layer.trainable = False

    model.compile(loss='categorical_crossentropy', optimizer=optimizers.RMSprop(lr=1e-5), metrics=['acc'])
    history = model.fit_generator(train_generator, steps_per_epoch=3, epochs=5)

    model.save('final.h5')



keywords = query1 + "," + query2
downloadImages(keywords)
defineModel()

