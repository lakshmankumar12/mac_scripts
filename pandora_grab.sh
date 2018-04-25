#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

result=$(osascript $DIR/pandora_grab.applescript)

if [ $? -ne 0 ] ; then
    echo "No cigar :("
else
    python3 $DIR/pandora_grab.py <(echo $result) /tmp/a.html
fi


