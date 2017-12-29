#!/bin/bash

result=$(osascript <<EOF
    tell application "Google Chrome"
        set found_video to false
        set value to "inf"
        set foundh to "unknown"
        set proph to 
        set window_list to every window
        repeat with the_window in window_list
            if found_video is equal to true then
                exit repeat
            end if
            set tab_list to every tab in the_window
            repeat with the_tab in tab_list
                if the title of the_tab contains "Pandora Plus" then
                    tell the_tab
                        execute javascript "var h = document.querySelector('.Tuner__VolumeDurationControl');"
                        set foundh to (execute javascript " var result=\"not-found\"; if ( h != null ) { result=\"found\"; }; result;")
                        set value to (execute javascript " var result = h.value; result; ")
                    end tell
                    set found_video to true
                    exit repeat
                end if
            end repeat
        end repeat
    end tell
    return value & ":" & foundh
EOF
)

if [ $? -ne 0 ] ; then
    echo "No cigar :("
else
    echo "result: $result"
fi

