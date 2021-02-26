cat ../fulljs.json | jq -r '.graphic_defines | .[] | .graphic' | grep 'Icons/Prestige/2021/Icon_Talents2021' > "source"
