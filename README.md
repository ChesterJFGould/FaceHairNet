# FaceHairNet

### Prerequisite
Both the latest release of python with Tensorflow2 installed as well as
[Python3.7](https://www.python.org/downloads/release/python-370/) installed as
`python3.7` with Tensorflow1 installed.

Download the [HairNet pretrained model](https://drive.google.com/file/d/1jHnkiY2GL-nwACSP8g80RIQI35tt-YDm/view?usp=sharing)
into `modelGen/model`.

### How to run
`./gen.sh <input image> <output model>`

For example:
`./gen.sh test.jpg test.obj`

### Licence


# [HairNet](https://github.com/pielet/HairNet.git)

### Report Summary
+ Data Preprocessing and Hair sampling: They used 300 3D hair models provided by [USC-HairSalon](http://www-scf.usc.edu/~liwenhu/SHM/database.html). Rotating around the z-axis at random angles, obtain 2D hair images facing various direction. 2D hair images represent the curvature of the hair strands with color variation from blue to red. The position and curvature data of sampled hair root and corresponding hair strand is stored in HDF5 file.  In this process they obtained 6 orientation maps from each hair model.  
+ Hair Prediciton Network: The network is implemented by Tensorflow. It first encodes the input image to a latent vector. For the encoder, they used the convolutional layers to extract the high-level features of the image. After obtain hair feature vector, decode the target hair strands from it. The decoder generate the hair strands in two steps. First the hair feature vector is decoded into multiple strand feature vectors by deconvoultional layers. Each strand feature vector is further decoded into the a stand geometry by the same multi-layer fully connected network.

### Changes We Made
+ `--mode gen --input <input_file> --output <output_file>` generates a 3d hair
  model into `<output_file>` based on `<input_file>`.
+ `--mode demo` now saves the generated `obj` file to `test.obj` in the working
  directory. This should become a separate mode.

More details can be found in their report which is on this github: https://github.com/pielet/HairNet.git.

# [PRNet](https://github.com/YadiraF/PRNet.git) (Face Model)

### Report Summary 
+ 3D Face Representation: They proposed UV position map as the presentation of full 3D facial structure with alignment information. UV position map is a 2D image recording 3D positions of all points in UV space. This is the case of using UV space to store the 3D position of points from 3D face model aligned with corresponding 2D facial image. The ground truth 3D facial shape exactly matches the face in the 2D image when projected to the x-y plane, so the position map is represented by pos(u,v) = (x,y,z) where (u, v) represents the UV coordinate of a point in face surface.
+ Network Architecture: They employed an encoder-decoder structure to learn the transfer function that transfers the input RGB image into position map image. The encoder part of the network begins with one convolution layer followed by 10 residual blocks which reduce the 256 × 256 × 3 input image into 8 × 8 × 512 feature maps. The decoder part contains 17 transposed convolution layers to generate the predicted 256 × 256 × 3 position map. In order to learn the parameters of the network, they built a loss function to measure the difference between ground truth position map and the network output. Since central region of face has more discriminative features than other regions, they employed a weight mask to form our loss function. The position of 68 facial keypoints has the highest weight, so that to ensure the network to learn accurate locations of these points.


More details can be found in their report which is on this github: https://github.com/YadiraF/PRNet.git.

