cat ../fulljs.json | jq -r '.graphic_defines | .[] | .graphic' | grep 'Icons/Prestige/2022/Icon_Talents2022' > "source"
