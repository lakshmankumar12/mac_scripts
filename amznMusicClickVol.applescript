#!/usr/bin/osascript

tell application "Google Chrome"
    set found_tab to false
    set amazonUrl to "https://music.amazon.in/"
    repeat with w in windows
        repeat with t in tabs of w
            if URL of t starts with amazonUrl then
                tell t
                    execute javascript "var h = document.querySelector('[aria-label=\"Volume\"]');"
                    execute javascript "h.click()"
                    return
                end tell
            end if
        end repeat
    end repeat
end tell

