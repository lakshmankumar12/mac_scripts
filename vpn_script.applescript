#!/usr/bin/osascript

#reference: https://neo.works/2017/How-to-login-Cisco-VPN-automatically-on-macOS-High-Sierra/

set vpn_name to "'Aryaka Bangalore'"
set user_name to "lakshman.narayanan"
set passwd to system attribute "MYPASSWD"

tell application "System Events"
    set rc to do shell script "scutil --nc status " & vpn_name
    if rc starts with "Disconnected" then
        do shell script "scutil --nc start " & vpn_name & " --user " & user_name
        delay 3
        keystroke tab
        keystroke return
        set theResponse to display dialog "Did vpn pop up?" buttons {"Don't Continue", "Continue"} default button "Continue" cancel button "Don't Continue"
        if button returned of theResponse is "Continue" then
            do shell script "scutil --nc start " & vpn_name & " --user " & user_name
            delay 3
            keystroke passwd
            keystroke return
            delay 3
            keystroke tab
            keystroke return
        end if
    end if
end tell
