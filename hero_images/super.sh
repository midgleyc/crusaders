if [ $# -eq 0 ]; then
  echo "Usage: ./super.sh <hero name | skin name>"
  exit 1
fi

for i in "$@"; do
  ./master.sh $i
done
