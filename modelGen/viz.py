# Author: Shiyang Jia
# Co-Author: Chester JF Gould

import numpy as np
import matplotlib as matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D
import random

from dataloader import load_root, get_mean_std


def visualize(data_dir, image, pos_gt, pos, angle):

    # recover images and position
    rgb_image = np.zeros((256, 256, 3), dtype=int)
    rgb_image[..., [0, 2]] = image * 255
    pos_mean, pos_std, _, _ = get_mean_std(data_dir)
    pos_gt = pos_gt * pos_std + pos_mean
    pos = pos * pos_std + pos_mean

    # load root and mask
    root, mask = load_root(data_dir)
    rotate_root = rotate_y(root, angle)
    rotate_root = np.tile(rotate_root, [1, 1, 100])
    pos_gt += rotate_root
    pos += rotate_root

    fig = plt.figure(figsize=(18, 6))
    fig.set_tight_layout(False)
    gs = gridspec.GridSpec(1, 3)
    gs.update(wspace=0.05)
    plt.axis('off')

    # plot orientation map
    ax1 = plt.subplot(gs[0])
    ax1.imshow(rgb_image)

    # plot hair ground truth
    ax2 = plt.subplot(gs[1], projection='3d')
    show3Dhair(ax2, pos_gt, mask)

    # plot predict hair
    ax3 = plt.subplot(gs[2], projection='3d')
    show3Dhair(ax3, pos, mask)

    plt.show()


def visualize_real(data_dir, image, pos):

    # recover images and position
    rgb_image = np.zeros((256, 256, 3), dtype=int)
    rgb_image[..., [0, 2]] = image[0] * 255
    pos_mean, pos_std, _, _ = get_mean_std(data_dir)
    pos = pos * pos_std + pos_mean


    # load root and mask
    root, mask = load_root(data_dir)
    pos += np.tile(root, [1, 1, 100])
    pos[..., :3] = root

    fig = plt.figure(figsize=(10, 5))

    plt.axis('off')

    # plot orientation map
    ax1 = fig.add_subplot(121)
    # print(type(ax1.figure))
    # ax1.figure.figimage(rgb_image)
    # ax1.figure(rgb_image)
    ax1.imshow(rgb_image)

    # plot predict hair
    ax2 = fig.add_subplot(122, projection='3d')
    show3Dhair(ax2, pos, mask)
    saveObjHairFile("test.obj", pos, mask)

    # print("Showing plot")
    plt.show()


def rotate_y(root, angle):
    """ rotate root around y-axis
    Args:
        root: [32, 32, 3] 1024 points
        angle: radius
    Return:
        rotated root
    """
    root_x, root_z = root[..., 0], root[..., 2]
    rotate_root = np.zeros_like(root)
    rotate_root[..., 0] = np.cos(angle)*root_x - np.sin(angle)*root_z
    rotate_root[..., 1] = root[..., 1]
    rotate_root[..., 2] = np.sin(angle)*root_x + np.cos(angle)*root_z

    return rotate_root

def saveObjHairFile(fileName, strands, mask):
    """
    fileName: string
    strands: [32, 32, 300]
    mask: [32, 32] bool
    """
    strands = strands.reshape(-1, 300)
    mask = mask.reshape(-1)


    vertices = []

    hairWidth = 0.04
    scaledY = [0, hairWidth, 0]


    def cross(a, b):
	    ax = a[0]
	    ay = a[1]
	    az = a[2]
	    bx = b[0]
	    by = b[1]
	    bz = b[2]
	    return [ay * bz - az * by, az * bx - ax * bz, ax * by - bx * ay]

    def add(a, b):
        return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]

    for i in range(32*32):
        if mask[i]:
            for j in range(0, 300-3, 3):
                # transform from graphics coordinate to math coordinate
                z, y, x = [np.array( [strands[i, j+axis], strands[i, j+axis+3]] ) for axis in range(3)]
                vertex0 = [x[0], y[0] - 1.7, z[0]]
                vertex1 = [x[1], y[1] - 1.7, z[1]]
                # vertex2 = [n + hairWidth for n in vertex0]
                # vertex3 = [n + hairWidth for n in vertex1]
                vertex2 = add(cross(vertex0, scaledY), vertex0)
                vertex3 = add(cross(vertex1, scaledY), vertex1)

                vertices.extend([vertex0, vertex1, vertex2, vertex3])

    file = open(fileName, 'w')

    for vertex in vertices:
        file.write("v {0} {1} {2}\n".format(vertex[0], vertex[1], vertex[2]))

    for i in range(1, len(vertices) + 1, 4):
        file.write("f {0} {1} {2}\n".format(i, i + 1, i + 2))
        file.write("f {0} {1} {2}\n".format(i + 1, i + 2, i + 3))

    file.close()

def show3Dhair(axis, strands, mask):
    """
    strands: [32, 32, 300]
    mask: [32, 32] bool
    """
    strands = strands.reshape(-1, 300)
    mask = mask.reshape(-1)

    for i in range(32*32):
        if mask[i]:
            for j in range(0, 300-3, 3):
                # transform from graphics coordinate to math coordinate
                colours = ['red', 'blue', 'green']
                y, z, x = [np.array( [strands[i, j+axis], strands[i, j+axis+3]] ) for axis in range(3)]
                axis.plot(x, y, z, linewidth=0.2, color=random.choice(colours))

    RADIUS = 0.3  # space around the head
    xroot, yroot, zroot = 0, 0, 1.65
    axis.set_xlim3d([-RADIUS+xroot, RADIUS+xroot])
    axis.set_ylim3d([-RADIUS+yroot, RADIUS+yroot])
    axis.set_zlim3d([-RADIUS+zroot, RADIUS+zroot])

    # Get rid of the ticks and tick labels
    axis.set_xticks([])
    axis.set_yticks([])
    axis.set_zticks([])

    axis.get_xaxis().set_ticklabels([])
    axis.get_yaxis().set_ticklabels([])
    axis.set_zticklabels([])
    axis.set_aspect('auto')

    """
    # Get rid of the panes (actually, make them white)
    white = (1.0, 1.0, 1.0, 0.0)
    axis.w_xaxis.set_pane_color(white)
    axis.w_yaxis.set_pane_color(white)
    axis.w_zaxis.set_pane_color(white)

    # Get rid of the lines in 3d
    axis.w_xaxis.line.set_color(white)
    axis.w_yaxis.line.set_color(white)
    axis.w_zaxis.line.set_color(white)
    """
