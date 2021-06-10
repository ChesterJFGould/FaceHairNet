#! /bin/sh

convertedImage="$(mktemp).png"
maskedImage="$(mktemp).png"

convert "$1" -scale 256x256 "$convertedImage"

python mask.py "$convertedImage" "$maskedImage"

python3.7 main.py "$maskedImage" "$2"
