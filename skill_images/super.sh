if [ $# -eq 0 ]; then
  echo "Usage: ./super.sh <hero name>"
  exit 1
fi

for i in "$@"; do
./master.sh $i

skillFolder="$OUTPUT_BASE_DIR_SKILLS/$i"
mkdir "$skillFolder"
mv $OUTPUT_BASE_DIR_SKILLS/*.png "$skillFolder"
done
