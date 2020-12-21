for f in swfs/*; do
  filename=$(basename $f)
  imageName=$(echo $filename | cut -d'.' -f1)
  ../hero_images/swf2svg.py --swf "$f" --svg "svgs/$imageName.svg"
  echo 'Prettifying'
  svgo --pretty "svgs/$imageName.svg"
done
