A storage location for several scripts.

# changelog.sh

When run, turns the latest changelogs into a format ready to be copied onto the wiki.

# generate\_equip\_page.py <id>[, <id>...]

Takes a number of IDs for equipment, generates wiki pages.

Find the latest ID by running:

> cat fulljs.json | jq '.loot\_defines | .[-1]'

# get\_skill\_images.sh "<hero name>"

Creates larger-scale wiki copyable PNG images for skills.

Requires `jq`

Requires several environment variables:
```
FULLJS # the json output of https://idleps18.djartsgames.ca/~idle/post.php?current_version=1&dl=0.22&call=getDefinitions. You can add a &filter to decrease the bytes
OUTPUT_BASE_DIR # where the final images should be saved (in a folder with the hero name)
```
