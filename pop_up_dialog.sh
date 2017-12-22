#!/bin/bash

text="$1"

if [ -z "$1" ] ; then
    text="Nothing was set"
fi

result=$(osascript <<EOF
    set theDialogText to "Hey! " & "$text" & "."
    display dialog theDialogText
EOF
)

if [ $? -ne 0 ] ; then
    echo "No cigar :("
fi

