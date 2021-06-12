import numpy as np
import os
import sys
from glob import glob
import scipy.io as sio
from skimage.io import imread, imsave
from skimage.transform import rescale, resize
from time import time
import argparse
import ast

from api import PRN

from utils.estimate_pose import estimate_pose
from utils.rotate_vertices import frontalize
from utils.render_app import get_visibility, get_uv_mask, get_depth_image
from utils.write import write_obj_with_colors, write_obj_with_texture

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

gpuNum = "0"

def main():
	# ---- init PRN
	os.environ['CUDA_VISIBLE_DEVICES'] = gpuNum # GPU number, -1 for CPU
	prn = PRN(True)

	inFile = sys.argv[1]
	outFile = sys.argv[2]

	# read image
	image = imread(inFile)
	[h, w, c] = image.shape
	if c>3:
		image = image[:,:,:3]

	# the core: regress position map
	max_size = max(image.shape[0], image.shape[1])
	if max_size > 1000:
		image = rescale(image, 1000./max_size)
		image = (image*255).astype(np.uint8)
	pos = prn.process(image) # use dlib to detect face

	image = image / 255.

	if pos is None:
		return

	# 3D vertices
	vertices = prn.get_vertices(pos)

	save_vertices = vertices.copy()
	save_vertices[:,1] = h - 1 - save_vertices[:,1]

	# corresponding colors
	colors = prn.get_colors(image, vertices)

	#save 3d face(can open with meshlab)
	write_obj_with_colors(outFile, save_vertices, prn.triangles, colors)

if __name__ == '__main__':
	main()
