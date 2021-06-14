#! /bin/sh

inputImage="$(mktemp).png"
convert "$1" -scale 256x256! "$inputImage"

outputImage="$(realpath $2)"


# Generate Hair

cd modelGen/

maskedImage="$(mktemp).png"
hairModel="$(mktemp).obj"

## Generate Masked Image
python mask.py "$inputImage" "$maskedImage"

## Generate Hair Model
python3.7 main.py "$maskedImage" "$hairModel"

cd ..

# Generate Face

cd PRNet-master/

faceModel="$(mktemp).obj"

python3.7 gen.py "$inputImage" "$faceModel"

cd ..

# Combined Hair and Face

cd combineModels/

python combineFaceAndHairObjFiles.py "$faceModel" "$hairModel" "$outputImage"

cd ..

# Cleanup

rm -f "$inputImage"
rm -f "$maskedImage"
rm -f "$hairModel"
rm -f "$faceModel"
