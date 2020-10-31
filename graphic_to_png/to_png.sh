#!/bin/bash

base=$(basename $1)

wget "http://idlemaster.djartsgames.ca/~idle/Graphics/$1.swf" -O "$base.swf"
../hero_images/swf2svg.py --swf "$base.swf" --svg "$base.svg"

width=$(grep -oe'width="\([0-9]*\)px"' "$base.svg" | sed -n 's/width="\([0-9]\+\)px"/\1/p')
((width *= 4))
height=$(grep -oe'height="\([0-9]*\)px"' "$base.svg" | sed -n 's/height="\([0-9]\+\)px"/\1/p')
((height *= 4))

rsvg-convert -a -w $width -h $height "$base.svg" > "$base.png"

mv "$base.png" "/mnt/c/Users/dad/Pictures/crusaders/raw_images"

rm *.swf *.svg
