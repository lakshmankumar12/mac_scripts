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
                    execute javascript "var h = document.querySelector('[data-qa=\"thumbs_down_button\"]'); h.click()"
                    set resultStr to "Clicked thumbs down in Pandora"
                    return resultStr
                end tell
            end if
            if URL of t starts with youtubeUrl then
                return
            end if
            if URL of t starts with saavnUrl then
                tell t
                    execute javascript "var h = document.querySelector('#dislike');"
                    execute javascript "h.click()"
                    set resultStr to "Clicked dislike in Saavn"
                    return resultStr
                end tell
            end if
            if URL of t starts with spotifyUrl then
                tell t
                    execute javascript "var h = document.querySelector('[title=\"Thumbs down\"]'); h.click()"
                    set resultStr to "Clicked Thumbs Down in Spotify"
                    return resultStr
                end tell
            end if
        end repeat
    end repeat
end tell
