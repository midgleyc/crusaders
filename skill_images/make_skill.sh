#!/bin/bash

IMAGE=$2
TYPE=$1

echo "Converting $IMAGE of type $1"
imageName=$(echo $IMAGE | cut -d'.' -f1)
./convert_svg.py --svg $IMAGE -n

width=$(grep -oe'width="\([0-9]*\)px"' $imageName.svg | sed -n 's/width="\([0-9]\+\)px"/\1/p')
((width *= 4))
height=$(grep -oe'height="\([0-9]*\)px"' $imageName.svg | sed -n 's/height="\([0-9]\+\)px"/\1/p')
((height *= 4))

rsvg-convert -a -w $width -h $height $imageName.svg  > $imageName.png
mogrify -background none -resize 260x260 -gravity center -extent 260x260 $imageName.png

if [ "$TYPE" = "formation" ]; then
composite -gravity center -geometry 260x260+0 $imageName.png "./backgrounds/formation.png" compose_$imageName.png
elif [ "$TYPE" = "ability" ]; then
composite -gravity center -geometry 260x260+0 $imageName.png "./backgrounds/ability.png" compose_$imageName.png
elif [ "$TYPE" = "upgrade" ]; then
composite -gravity center -geometry 260x260+0 $imageName.png "./backgrounds/upgrade.png" compose_$imageName.png
fi

mogrify -trim +repage compose_$imageName.png

if [ -f compose_$imageName.png ]; then
mv compose_$imageName.png working/$(echo $imageName | rev | cut -d '_' -f 1 | rev).png
fi
