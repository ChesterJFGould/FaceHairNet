# install requirements
# assuming running at network directory

# if remove # below if want to set up virtual env
# conda create -n PRNet python=3.6
pip install -r requirement.txt

# my pip can't get dlib installed
conda install -c conda-forge dlib

wget https://doc-14-1o-docs.googleusercontent.com/docs/securesc/ss6561b2vvee219fkaginn3i2gisqoot/9lmd10fkldfa40jee8d03ajhublj0kfn/1623392850000/13367573649401534672/09602463561024371320Z/1UoE-XuW1SDLUjZmJPkIZ1MLxvQFgmTFH?e=download&nonce=puf4rcdku2kmo&user=09602463561024371320Z&hash=ukulfrsr04jv8pqcvih7kadcirgt5h9s

mkdir Data
mkdir Data/net-data

mv 256_256_resfcn256_weight.data-00000-of-00001 Data/net-data
