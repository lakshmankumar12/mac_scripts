#!/usr/bin/env python3

import subprocess

def getFromSpotifyTrack(what, from_track=True):
    track = 'of the current track'
    if not from_track:
        track = ''
    cmd = '''osascript -e 'tell application "spotify" to get {} {}' '''.format(what,track)
    output = subprocess.run(cmd,shell=True,capture_output=True)
    unicodeStr = output.stdout.decode('utf-8')
    return unicodeStr.strip()

def getDuration():
    duration=getFromSpotifyTrack('duration')
    duration=int(duration)
    duration=duration//1000
    duration_min=duration // 60
    duration_sec=duration % 60
    return "{}:{}".format(duration_min,duration_sec)

def getCurrPosition():
    current=getFromSpotifyTrack('player position', from_track=False)
    current=float(current)
    current=int(current)
    current_min=current//60
    current_sec=current%60
    return "{}:{}".format(current_min,current_sec)

def getPlayerState():
    state=getFromSpotifyTrack('player state', from_track=False)
    if state == 'playing':
        return ""
    return "\n" + state.upper()

trk=getFromSpotifyTrack('name')
artist=getFromSpotifyTrack('artist')
album=getFromSpotifyTrack('album')
duration=getDuration()
current=getCurrPosition()
state=getPlayerState()
volume=getFromSpotifyTrack('sound volume', from_track=False)
print ( "Track:  {}\n"
        "Artist: {}\n"
        "Album:  {}\n"
        "Time:   {} of {}{}\n"
        "Volume: {}".format(trk,artist,album,current,duration,state,volume))
