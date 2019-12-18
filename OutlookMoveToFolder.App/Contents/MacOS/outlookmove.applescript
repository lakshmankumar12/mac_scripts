#!/usr/bin/osascript
activate application "Microsoft Outlook"
tell application "System Events"
	tell process "Microsoft Outlook"
		click menu item "Choose Folder..." of menu "Move" of menu item "Move" of menu "Message" of menu bar item "Message" of menu bar 1
	end tell
end tell
