#!/usr/bin/osascript

set doc to ""
tell application "Google Chrome"
    set found_tab to false
    set targetUrl to "https://www.pandora.com"
    set window_list to every window
    repeat with the_window in window_list
        if found_tab is equal to true then
            exit repeat
        end if
        set tab_list to every tab in the_window
        repeat with the_tab in tab_list
            if ((URL of the_tab) contains targetUrl) then
                tell the_tab
                    (execute javascript "var now_playing = document.querySelector('[data-qa=\"header_now_playing_link\"]'); now_playing.click();")
                    set doc to (execute javascript "var h = document.documentElement.innerHTML; h;")
                end tell
                set found_tab to true
                exit repeat
            end if
        end repeat
    end repeat
end tell
return doc
