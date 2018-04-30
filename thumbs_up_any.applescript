#!/usr/bin/osascript

tell application "Google Chrome"
    set spotifyUrl to "https://open.spotify.com"
    set pandoraUrl to "https://www.pandora.com"
    set saavnUrl to "https://www.saavn.com"
    set youtubeUrl to "https://www.youtube.com/"
    set resultStr to ""
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
                return
            end if
            if URL of t starts with saavnUrl then
                tell t
                    execute javascript "var h = document.querySelector('#like');"
                    execute javascript "h.click()"
                    set resultStr to "Clicked like in Saavn"
                    return resultStr
                end tell
            end if
            if URL of t starts with spotifyUrl then
                tell t
                    execute javascript "var h = document.querySelector('[title=\"Thumbs up\"]'); h.click()"
                    set resultStr to "Clicked Thumbs up in Spotify"
                    return resultStr
                end tell
            end if
        end repeat
    end repeat
end tell
