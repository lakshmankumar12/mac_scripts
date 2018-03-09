#!/bin/bash

result=$(osascript <<EOF
    tell application "Google Chrome"
        set songtitle to ""
        set songartist to ""
        set songalbum to ""
        set elapsedtime to ""
        set tottime to ""
        set playing to ""
        set found_video to false
        set window_list to every window
        repeat with the_window in window_list
            if found_video is equal to true then
                exit repeat
            end if
            set tab_list to every tab in the_window
            repeat with the_tab in tab_list
                if the title of the_tab contains "Pandora" then
                    tell the_tab
                    set songtitle to (execute javascript "var outputtitle = document.querySelector('[data-qa=\"playing_track_title\"]').innerHTML; outputtitle;")
                    set songartist to (execute javascript "var outputartist = document.querySelector('[data-qa=\"playing_artist_name\"]').innerHTML; outputartist;")
                    set songalbum to (execute javascript "var outputalbum = document.querySelector('[data-qa=\"playing_album_name\"]').innerHTML; outputalbum;")
                    set elapsedtime to (execute javascript "var elapsedtime = document.querySelector('[data-qa=\"elapsed_time\"]').innerHTML; elapsedtime;")
                    set tottime to (execute javascript "var tottime = document.querySelector('[data-qa=\"remaining_time\"]').innerHTML; tottime;")
                    set playing to (execute javascript "var result = 'Playing'; var h = document.querySelector('[aria-label=\"Pause\"]'); if (h == null) { result = 'Paused'; } ; result ;")
                    end tell
                    set found_video to true
                    exit repeat
                end if
            end repeat
        end repeat
    end tell
    return songtitle & "\`" & songartist & "\`" & songalbum & "\`" & elapsedtime & "\`" & tottime & "\`" & playing
EOF
)

if [ $? -ne 0 ] ; then
    echo "No cigar :("
else
    python ~/github/mac_scripts/parse_pandora_info.py <(echo -n $result)
fi

