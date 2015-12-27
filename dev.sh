PREFIX=$(cd "$(dirname "$0")"; pwd)


python $PREFIX/css_js.py

PROGRAM=$PREFIX/dev.py
ps x -u $USER|ack $PROGRAM|awk  '{print $1}'|xargs kill -9 > /dev/null 2>&1
ps x -u $USER|ack 'jitter'|awk  '{print $1}'|xargs kill -9 > /dev/null 2>&1
coffee -o  $PREFIX/js $PREFIX/coffee
python $PROGRAM
echo 'aaaaa'

