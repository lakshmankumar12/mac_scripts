#!/usr/bin/env python3

import mac_script_helper
import bs4
import sys

bwsrTab = mac_script_helper.BrowserTab('https://open.spotify.com')

js = [
        '''execute javascript "var outputtitle_div = document.querySelector('.track-info__name');var outputtitle_a = outputtitle_div.querySelector('a'); outputtitle_a.click(); outputtitle_div;"'''
     ]

err,page,_ = bwsrTab.sendCommands(js)
if err != 0:
    print ("Trouble in getting page-info from pandora")
    sys.exit(1)

js = [
      mac_script_helper.SaveDocCmd,
     ]

err,page,_ = bwsrTab.sendCommands(js)
if err != 0:
    print ("Trouble in getting page-info from saavn")
    sys.exit(1)

pageSoup = bs4.BeautifulSoup(page, 'html.parser')
with open ('/tmp/a.html','w') as fd:
    fd.write(pageSoup.prettify())

trackInfo = pageSoup.findAll("div", {"class": "track-info"})
if not trackInfo:
    print ("Is spotify running?")
    sys.exit(1)
else:
    trackInfo = trackInfo[0]
albumInfo1 = pageSoup.findAll("div", {"class": "media-bd"})
albumInfo2 = None
albumArtist2 = None
year2 = None
if albumInfo1:
    albumInfo2 = albumInfo1[0].findAll("h2")[0]
    albumArtist1 = albumInfo1[0].findAll("div", {"class": "entity-name"})[0]
    albumArtist2 = albumArtist1.findAll("span")[1]
    year1 = albumInfo1[0].findAll("p", {"class": "entity-additional-info"})
    if year1:
        year2 = year1[0]
trackName = trackInfo.findAll("div", {"class": "track-info__name"})[0]
artistNames = trackInfo.findAll("div", {"class": "track-info__artists"})[0]
progress = pageSoup.findAll("div", {"class": "playback-bar__progress-time"})

pause_btn = pageSoup.findAll("button", {"title": "Pause"})
if not pause_btn:
    play_btn = pageSoup.findAll("button", {"title": "Play"})
    if play_btn:
        play_status = "Paused"
    else:
        play_status = "Unknown"
else:
    play_status = "Playing"

title = trackName.get_text()
artist = artistNames.get_text()
if albumInfo2:
    album = albumInfo2.get_text()
else:
    album = ""
if albumArtist2:
    albumArtist = albumArtist2.get_text()
else:
    albumArtist = ""
if year2:
    year = year2.get_text()
else:
    year = ""
elapsed = progress[0].get_text()
total = progress[1].get_text()

print ('''\
Spotify Song Info
-----------------
Title:        {}
Artist:       {}
Album:        {}
Album-artist: {}
Year:         {}
Elapsed:      {}
Total:        {}
Playing:      {}'''.format(title, artist, album, albumArtist, year, elapsed, total, play_status))

all_tracks = []
maxwidth = 10
all_tracks_div = pageSoup.findAll("div", {"class": ["tracklist-col", "name"]})
if all_tracks_div:
    for d in all_tracks_div:
        track_name = d.findAll("span", {"class": "tracklist-name"})
        if track_name:
            t = track_name[0].get_text()
            maxwidth = max(maxwidth,len(t))
            artists = d.findAll("span", {"class": "second-line"})
            if artists:
                a = artists[0].get_text()
                all_tracks.append((t,a))

if all_tracks:
    print ("Tracks in Album:")
    print ("----------------")
    for (t,a) in all_tracks:
        print ("{:{width}} | {}".format(t,a,width=maxwidth))
