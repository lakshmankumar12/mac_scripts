#!/bin/bash

result=$(osascript /Users/lakshman.narayanan/github/mac_scripts/get_song_info_spotify.applescript)

if [ $? -ne 0 ] ; then
    echo "No cigar :("
else
    python3 ~/github/mac_scripts/parse_spotify_info.py <(echo $result) /tmp/a.html
fi


