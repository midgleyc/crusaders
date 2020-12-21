(
cd swfs
for f in $(cat ../source); do
  wget "http://idlemaster.djartsgames.ca/~idle/swf/Graphics/$f.swf";
done
)
