#!/usr/bin/osascript

tell application "Google Chrome"
    set found_tab to false
    set spotifyUrl to "https://open.spotify.com"
    set pandoraUrl to "https://www.pandora.com"
    set saavnUrl to "https://www.saavn.com"
    set youtubeUrl to "https://www.youtube.com/"
    repeat with w in windows
        repeat with t in tabs of w
            if URL of t starts with pandoraUrl then
                tell t
                    execute javascript "var h = document.querySelector('[aria-label=\"Pause\"]');"
                    execute javascript "if(h == null) var h = document.querySelector('[aria-label=\"Play\"]');"
                    execute javascript "h.click()"
                    return
                end tell
            end if
            if URL of t starts with youtubeUrl then
                tell t
                    execute javascript "var h = document.querySelector('[aria-label=\"Pause\"]');"
                    execute javascript "if(h == null) var h = document.querySelector('[aria-label=\"Play\"]');"
                    execute javascript "h.click()"
                end tell
                return
            end if
            if URL of t starts with saavnUrl then
                tell t
                    execute javascript "var h = document.querySelector('#pause');"
                    execute javascript "h.click()"
                    return
                end tell
            end if
            if URL of t starts with spotifyUrl then
                tell t
                    execute javascript "var h = document.querySelector('[title=\"Pause\"]');"
                    execute javascript "if(h == null) var h = document.querySelector('[title=\"Play\"]');"
                    execute javascript "h.click()"
                    return
                end tell
            end if
        end repeat
    end repeat
end tell
