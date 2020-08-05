A storage location for several scripts.

# changelog.sh

When run, turns the latest changelogs into a format ready to be copied onto the wiki.

# generate\_equip\_page.py <id>[, <id>...]

Takes a number of IDs for equipment, generates wiki pages.

Find the latest ID by running:

> cat fulljs.json | jq '.loot\_defines | .[-1]'

# get\_skill\_icons.sh "<hero name>"

Creates larger-scale wiki copyable PNG images for skills.

Requires:
* `jq`,
* `ImageMagick` (for `composite` and `mogrify`)
* An SVG conversion script. This is based off [or's](https://gist.github.com/or/aabfb3ce33b4b7417dbf/), but adjusted to run on Python 3 (post Ubuntu 20, I can't install the deps for 2). The script requires:
 * [pycairo](https://github.com/pygobject/pycairo), which requires [cairo and its headers](https://pycairo.readthedocs.io/en/latest/getting_started.html)
 * [pyswf](https://github.com/timknip/pyswf), except that you want to run it on Python3, so you need to clone and install from there (use `pip install .`), and also to apply [tuomassalo's change to allow fonts without FontInfo](https://github.com/timknip/pyswf/pull/36) and [my change to allow export](https://github.com/timknip/pyswf/pull/49)
* `rsvg-convert`

Requires several environment variables:
```
FULLJS # the json output of https://idleps18.djartsgames.ca/~idle/post.php?current_version=1&dl=0.22&call=getDefinitions. You can add a &filter to decrease the bytes
OUTPUT_BASE_DIR # where the final images should be saved (in a folder with the hero name)
```
