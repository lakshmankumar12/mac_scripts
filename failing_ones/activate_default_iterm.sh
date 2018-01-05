#!/bin/bash

result=$(osascript <<EOF
    tell application "iTerm"
        repeat with the_window in window_list
            if the title of the_window contains "Default" then
                activate the_window
                exit repeat
            end if
        end repeat
    end tell
EOF
)

if [ $? -ne 0 ] ; then
    echo "No cigar :("
else
    echo "Activated"
fi

