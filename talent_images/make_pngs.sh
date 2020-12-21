for f in ./svgs_with_extras/*; do
  filename=$(basename $f)
  imageName=$(echo $filename | cut -d'.' -f1)
  finalName=$(echo $imageName | rev | cut -d'_' -f1 | rev)
  rsvg-convert -a -w 256 -h 256 "$f" > "pngs/$finalName.png"
done
