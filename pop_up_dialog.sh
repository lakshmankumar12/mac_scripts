#!/bin/bash

text="$1"

if [ -z "$1" ] ; then
    text="Nothing was set"
fi

text="Reminder at $(date +%H:%M) : ${text}"

result=$(osascript <<EOF
    set theDialogText to "Hey! " & "$text" & "."
    display dialog theDialogText with icon caution
EOF
)

if [ $? -ne 0 ] ; then
    echo "No cigar :("
fi

