cat ../fulljs.json | jq -r '.graphic_defines | .[] | .graphic' | grep 'Icons/Prestige/2020/Icon_Talents2020Dec' > "source"
