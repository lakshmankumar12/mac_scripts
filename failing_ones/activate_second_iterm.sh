result=$(osascript <<EOF
    tell application "iTerm"
        set wins to id of every window whose name contains "Anap-Console-Monitor"
        -- activate window wins
    end tell
EOF
)

if [ $? -ne 0 ] ; then
    echo "No cigar :("
else
    echo "result was : $result"
fi

