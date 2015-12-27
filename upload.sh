PREFIX=$(cd "$(dirname "$0")"; pwd)

jitter $PREFIX/coffee $PREFIX/js &
python $PREFIX/css_js.py
svn add $PREFIX/* --force
svn ci -m f
ps x -u $USER|ack 'jitter'|awk  '{print $1}'|xargs kill -9 > /dev/null 2>&1
hg fe 
hg ci -m f
hg push
