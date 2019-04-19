import os
import cv2 as cv
import numpy as np


def colorme(path_to_image, image_name):
    W_in = 224
    H_in = 224
    imshowSize = (640, 480)

    #os.getcwd() + '/DLPart' + '/
    # Select desired model
    net = cv.dnn.readNetFromCaffe(os.getcwd() + '/DLPart' + '/colorization_deploy_v2.prototxt',
                                  os.getcwd() + '/DLPart' + '/colorization_release_v2.caffemodel')

    pts_in_hull = np.load(os.getcwd() + '/DLPart' + '/pts_in_hull.npy')  # load cluster centers

    # populate cluster centers as 1x1 convolution kernel
    pts_in_hull = pts_in_hull.transpose().reshape(2, 313, 1, 1)
    net.getLayer(net.getLayerId('class8_ab')).blobs = [pts_in_hull.astype(np.float32)]
    net.getLayer(net.getLayerId('conv8_313_rh')).blobs = [np.full([1, 313], 2.606, np.float32)]

    image = cv.imread(path_to_image)
    img_rgb = (image[:, :, [2, 1, 0]] * 1.0 / 255).astype(np.float32)

    img = cv.cvtColor(img_rgb, cv.COLOR_RGB2Lab)

    img_l = img[:, :, 0]  # pull out L channel
    (H_orig, W_orig) = img.shape[:2]  # original image size

    # resize image to network input size
    img_rs = cv.resize(img_rgb, (W_in, H_in))  # resize image to network input size
    img_lab_rs = cv.cvtColor(img_rs, cv.COLOR_RGB2Lab)
    img_l_rs = img_lab_rs[:, :, 0]
    img_l_rs -= 50  # subtract 50 for mean-centering

    net.setInput(cv.dnn.blobFromImage(img_l_rs))
    ab_dec = net.forward()[0,:, :, :].transpose((1, 2, 0))  # this is our result

    (H_out, W_out) = ab_dec.shape[:2]
    ab_dec_us = cv.resize(ab_dec, (W_orig, H_orig))

    img_lab_out = np.concatenate((img_l[:, :, np.newaxis], ab_dec_us), axis=2)


    cur = cv.cvtColor(img_lab_out, cv.COLOR_Lab2BGR)
    img_bgr_out = np.clip(cur, 0, 1)
    img_bgr_out=img_bgr_out*255

    cv.imwrite('image/static/image/images/'+image_name,img_bgr_out)

    #imshow needs int bet 0 to 1 but imwrite needs bet 0 to 255 , and default color mode for opencv is BGR




#colorme('kid.jpg','abc')
