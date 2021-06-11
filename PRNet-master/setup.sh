# install requirements
# assuming running at network directory

# if remove # below if want to set up virtual env
# conda create -n PRNet python=3.6
pip install -r requirements.txt

# my pip can't get dlib installed
conda install -c conda-forge dlib

wget /uc?export=download&confirm=JZMp&id=1UoE-XuW1SDLUjZmJPkIZ1MLxvQFgmTFH
mkdir Data
mkdir Data/net-data

mv 256_256_resfcn256_weight.data-00000-of-00001 Data/net-data
