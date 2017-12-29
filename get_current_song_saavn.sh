#!/bin/bash

result=$(osascript <<EOF
    tell application "Google Chrome"
        set songtitle to ""
        set songartist to ""
        set songalbum to ""
        set elapsedtime to ""
        set tottime to ""
        set found_video to false
        set window_list to every window
        repeat with the_window in window_list
            if found_video is equal to true then
                exit repeat
            end if
            set tab_list to every tab in the_window
            repeat with the_tab in tab_list
                if the title of the_tab contains "Saavn" then
                    tell the_tab
                    set songtitle to (execute javascript "var outputtitle = document.querySelector('#player-track-name').innerHTML; outputtitle;")
                    set albumtitle to (execute javascript "var outputalbum = document.querySelector('#player-album-name').innerHTML; outputalbum;")
                    set singers to (execute javascript "var outputsingers = document.querySelector('#radio-singers').innerHTML; outputsingers;")
                    set elapsedtime to (execute javascript "var elapsedtime = document.querySelector('#track-elapsed').innerHTML; elapsedtime;")
                    set tottime to (execute javascript "var tottime = document.querySelector('#track-time').innerHTML; tottime;")
                    end tell
                    set found_video to true
                    exit repeat
                end if
            end repeat
        end repeat
    end tell
    return songtitle & "\`" & albumtitle & "\`" & singers & "\`" & elapsedtime & "\`" & tottime
EOF
)

if [ $? -ne 0 ] ; then
    echo "No cigar :("
else
    #echo "Orignal result: $result"
    python ~/github/mac_scripts/parse_saavn_info.py <(echo -n $result)
    #echo $result | awk -F\` ' {trackInfo = gensub(/<\/?a[^>]*>/,"","g",$1); albumInfo = gensub(/<\/?a[^>]*>/,"","g",$2); print "track:   " trackInfo "\nAlbum:   " albumInfo "\nElapsed: " $3 "\nTotal:   " $4} '
fi

