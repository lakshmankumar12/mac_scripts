#!/bin/bash

result=$(osascript <<EOF
            tell application "Google Chrome"
                set found_video to false
                set window_list to every window
                repeat with the_window in window_list
                    if found_video is equal to true then
                        exit repeat
                    end if
                    set tab_list to every tab in the_window
                    repeat with the_tab in tab_list
                        if the title of the_tab contains "Pandora" or the title of the_tab contains "Youtube" then
                            tell the_tab
                                execute javascript "var h = document.querySelector('[aria-label=\"Pause\"]');"
                                execute javascript "if(h == null) var h = document.querySelector('[aria-label=\"Play\"]');"
                                execute javascript "h.click()"
                            end tell
                            set found_video to true
                            exit repeat
                        end if
                        if the title of the_tab contains "Saavn" then
                            tell the_tab
                                execute javascript "var h = document.querySelector('#pause');"
                                execute javascript "h.click()"
                            end tell
                            set found_video to true
                            exit repeat
                        end if
                    end repeat
                end repeat
            end tell
EOF
)

if [ $? -ne 0 ] ; then
    echo "No cigar :("
else
    echo "Paused/Un-Paused: $result"
fi

