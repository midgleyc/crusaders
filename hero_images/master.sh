if [ $# -eq 0 ]; then
  echo "Usage: ./master.sh <hero name | skin name>"
  exit 1
fi

skin=""
echo 'Trying hero image'
graphic_id=$(< "$FULLJS" jq -e '.hero_defines | map(select(.name == "'"$*"'")) | .[0] | .graphic_id' -r)
if [ $? != 0 ]; then
  echo 'Trying skin image'
  graphic_id=$(< "$FULLJS" jq -e '.hero_skin_defines | map(select(.name == "'"$*"'")) | .[0] | .graphic_id' -r)
  if [ $? != 0 ]; then
    echo "Usage: ./master.sh <hero name>"
    exit 1
  fi
  skin="skin"
fi

echo 'Getting swf'
url=$(< $FULLJS jq -r '.graphic_defines | map(select(.id == '"$graphic_id"')) | .[0] | "http://idlemaster.djartsgames.ca/~idle/swf/Graphics/\(.graphic).swf"')

wget "$url" -O "$*.swf"
echo 'Making icon'
./make_icon.sh "$*.swf"
echo "Moving to $OUTPUT_BASE_DIR_HERO/$*/"
mkdir -p "$OUTPUT_BASE_DIR_HERO/$*/"
mv "$*.png" $OUTPUT_BASE_DIR_HERO
echo 'Producing smaller icons'
cp "$OUTPUT_BASE_DIR_HERO/$*.png" "$OUTPUT_BASE_DIR_HERO/$*/$*_256.png"
convert -resize 48x48 "$OUTPUT_BASE_DIR_HERO/$*/$*_256.png" "$OUTPUT_BASE_DIR_HERO/$*/$*_48.png"
if [ ! "$skin" ]; then
  convert -resize 24x24 "$OUTPUT_BASE_DIR_HERO/$*/$*_256.png" "$OUTPUT_BASE_DIR_HERO/$*/$*_24.png"
fi

rm *.swf *.svg
