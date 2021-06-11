import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

img_pth = "/home/jesus/projects/git_gizmos/PRNet/inp_img/face.png"
out_pth = "face.obj"

def main():
    img = plt.imread(img_pth)
    height,width,c = img.shape

    n = 0
    tri_pts = np.array(list(range(height*width))).reshape(height,width)
    with open(out_pth, "w") as f:


        for h in tqdm(range(height)):
            for w in range(width):
                s = 'v {} {} {} {} {} {}\n'.format(h, w, 0, img[h,w, 0], img[h,w, 1], img[h,w, 2])
                f.write(s)
        
        gap = 1
        for h in tqdm(range(gap,height,gap)):
            for w in range(gap,width,gap):
                s = 'f {} {} {}\n'.format(tri_pts[h-gap,w-gap], tri_pts[h-gap,w],tri_pts[h,w-gap])
                f.write(s)
                s = 'f {} {} {}\n'.format(tri_pts[h,w-gap], tri_pts[h-gap,w],tri_pts[h,w])
                f.write(s)

#        s = 'f {} {} {}\n'.format(tri_pts[0],tri_pts[2],tri_pts[1])
#        f.write(s)

#        s = 'f {} {} {}\n'.format(tri_pts[3],tri_pts[2],tri_pts[1])
#        f.write(s)

if __name__ == "__main__":
    main()
    
        

