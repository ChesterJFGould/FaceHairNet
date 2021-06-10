import glob
import time

import sys
import cv2
import os

stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
import tensorflow.keras as keras
sys.stderr = stderr

import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # Fuck you tensorflow
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

import numpy as np


def predict(image, height=224, width=224):
    # im = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    im = image

    im = im / 255
    im = cv2.resize(im, (height, width))
    im = im.reshape((1,) + im.shape)
    
    pred = model.predict(im)
    
    mask = pred.reshape((224, 224))

    return mask

def blackout(image, mask):
    mask[mask > 0.5] = 255
    mask[mask <= 0.5] = 0

    mask = cv2.resize(mask, (image.shape[1], image.shape[0]))
    mask_n = np.zeros_like(image)
    mask_n[:, :, 0] = mask
    mask_n[:, :, 1] = mask
    mask_n[:, :, 2] = mask

    # print(mask_n.shape)
    # print(img.shape)

    alpha = 0.8
    beta = (1.0 - alpha)
    dst = cv2.bitwise_and(image, mask_n)

    return dst


if __name__ == '__main__':

    # model = keras.models.load_model('models/hairnet_matting.hdf5')
    fileName = sys.argv[1]

    model = keras.models.load_model('./segModel/checkpoint.hdf5')

    img = cv2.imread(fileName)

    mask = predict(img)

    d1 = time.time()
    dst = blackout(img, mask)

    cv2.imwrite(sys.argv[2], dst)
