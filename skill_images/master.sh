if [ $# -eq 0 ]; then
  echo "Usage: ./master.sh <hero name>"
  exit 1
fi

hero_id=$(cat $FULLJS | jq '.hero_defines | map(select(.name == "'"$*"'")) | .[0] | .id' -r)
if [ -z "$hero_id" ]; then
  echo "Usage: ./master.sh <hero name>"
  exit 1
fi

cat $FULLJS | jq -r  '. as $in | .upgrade_defines | map(select(.hero_id == '"$hero_id"')) | map({graphic: .graphic_id, effect: {type: (.effect / "," | .[0]), id: (.effect / "," | .[1]) | tonumber}}) | map({graphic, effect: (if .effect.type == "unlock_formation_ability" then (if ((.effect.id as $e | $in.formation_ability_defines | map(select($e == .id)) | .[0]).properties as $properties | (try $properties.show_as_upgrade catch null)) then "upgrade" else "formation" end) elif .effect.type == "unlock_ability" then "ability" else "upgrade" end)}) | map({graphic: (.graphic as $g | $in.graphic_defines | map(select($g == .id)) | .[0]).graphic, effect}) | .[] | "\(.effect) http://idlemaster.djartsgames.ca/~idle/swf/Graphics/\(.graphic).swf"' | xargs -L1 ./download_skills.sh

rm *.png *.swf *.svg
