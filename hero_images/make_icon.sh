#!/bin/bash

IMAGE=$1

echo "Converting $IMAGE"
imageName=$(echo $IMAGE | cut -d'.' -f1)
./swf2svg.py --swf "$IMAGE" --svg "$imageName.svg" --frame 3

echo 'Prettifying'
svgo --pretty "$imageName.svg"

echo 'Adding icon parts'
./add_extra_svg_parts.py "$imageName.svg"

echo 'Converting to PNG'
rsvg-convert -a -w 256 -h 256 "$imageName.svg" > "$imageName.png"
