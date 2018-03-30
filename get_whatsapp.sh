#!/bin/bash

result=$(osascript <<EOF
    tell application "Google Chrome"
        set docoutput to "unset"
        set found_tab to false
        set window_list to every window
        repeat with the_window in window_list
            if found_tab is equal to true then
                exit repeat
            end if
            set tab_list to every tab in the_window
            repeat with the_tab in tab_list
                if the title of the_tab contains "WhatsApp" then
                    tell the_tab
                    set docoutput to (execute javascript "var bodydoc = document.getElementsByTagName('body')[0].innerHTML; bodydoc")
                    end tell
                    set found_tab to true
                    exit repeat
                end if
            end repeat
        end repeat
    end tell
    return docoutput
EOF
)

if [ $? -ne 0 ] ; then
    echo "No cigar :("
else
    echo "Doc was:"
    echo $result | python ~/github/mac_scripts/parse_whatsapp_info.py
fi

