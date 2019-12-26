#!/usr/bin/osascript

set appName to "spotify"

if application appName is running then
    tell application "spotify"
        next track
    end tell
    return "Running"
else
    return "Not Running"
end if
