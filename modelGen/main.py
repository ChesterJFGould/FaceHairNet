# Author: Shiyang Jia

import os
import cv2
import time
import math
import random
import sys
import numpy as np

import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # Fuck you tensorflow
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from six.moves import xrange

from dataloader import Dataloader, load_real_image, get_mean_std, load_root
from model import HairModel
from viz import visualize, visualize_real, saveObjHairFile

data_dir = "./data"
model_path = "./model/ckpt-7840"

learning_rate = 1e-4
epochs = 1

def create_model(session):
    # Create model and initialize it or load its parameters in a session

    # Args:
    #     session: tensorflow session
    # Return:
    #     model: HairNet model (created / loaded)

    model = HairModel(learning_rate, epochs, "/dev/null") # os.path.join(args.output_dir, 'summary'))

    # load a previously saved model
    # ckpt_path = os.path.join(args.output_dir, 'ckpt')
    # ckpt = tf.train.latest_checkpoint(ckpt_path)
    ckpt = model_path
    if ckpt:
        # print('loading model {}'.format(os.path.basename(ckpt)))
        model.saver.restore(session, ckpt)
        return model
    else:
        raise(ValueError, 'can NOT find model')

def gen(inFile, outFile):
    img = cv2.imread(inFile)
    img = dirFilter(img)
    img_data = img.astype(np.float64) / 255
    img_data = img_data[:, :, (2, 0)]
    cheat_y = np.zeros((1, 32, 32, 500))

    config = tf.ConfigProto(device_count={'GPU': 1}, allow_soft_placement=True)
    with tf.Session(config=config) as sess:
	    model = create_model(sess)
	    pos, curv, _, = model.step(sess, img_data, cheat_y, False)

    pos_mean, pos_std, _, _ = get_mean_std(data_dir)
    pos = pos * pos_std + pos_mean

    root, mask = load_root(data_dir)
    pos += np.tile(root, [1, 1, 100])
    pos[..., :3] = root

    saveObjHairFile(outFile, pos, mask)

def dirFilter(img):
    def gabor(img, theta):
            """
            g_kernel = cv2.getGaborKernel( (7, 7) # kernel size
                                         , 0.9 # sigma | gaussian std. dev.
                                         , theta # theta | orientation angle
                                         , 2.2 # lambda | sinusoidal wavelength
                                         , 0.5 # gamma | spatial aspect ratio
                                         , 0 # psi | phase offset
                                         , ktype=cv2.CV_32F ) # kernel type
            """
            g_kernel = cv2.getGaborKernel( (31, 31) # kernel size
                                         , 3.5 # sigma | gaussian std. dev.
                                         , theta # theta | orientation angle
                                         , 4 # lambda | sinusoidal wavelength
                                         , 0.5 # gamma | spatial aspect ratio
                                         , 0 # psi | phase offset
                                         , ktype=cv2.CV_32F ) # kernel type
            # """

            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return cv2.filter2D(img, cv2.CV_8UC2, g_kernel)

    # print(img.shape)
    img_prime = img
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    n = 100
    images = np.ndarray(shape = (n,) + img.shape, dtype = 'uint8')

    for i in range(n):
        theta = i * np.pi / n
        images[i] = gabor(img, theta)

    # img_prime = gabor(img_prime, 0)

    for x in range(images.shape[1]):
        for y in range(images.shape[2]):
            vals = []
            for i in range(images.shape[0]):
                theta = i * np.pi / n
                # vals.append((math.sqrt(abs(images[i, x, y])), theta))
                vals.append((images[i, x, y], theta))
            brightness, theta = max(vals)
            scale = 2
            blue = brightness * abs(math.cos(theta + math.pi / 4)) * scale
            red = brightness * abs(math.cos(theta - math.pi / 4)) * scale
            img_prime[x, y] = [red, 0, blue]

    return img_prime

def filterTest(inFile, outFile):
    img = cv2.imread(inFile)
    img = dirFilter(img)
    cv2.imwrite(outFile, img)

def main():
    gen(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()
