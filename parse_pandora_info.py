#!/usr/bin/env python3

import mac_script_helper
import bs4
import sys

bwsrTab = mac_script_helper.BrowserTab('https://www.pandora.com/')

js = [
       '''execute javascript "var now_playing = document.querySelector('[data-qa=\\"header_now_playing_link\\"]'); now_playing.click();"'''
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

trackDiv = pageSoup.findAll("a", {"class": "nowPlayingTopInfo__current__trackName"})
if not trackDiv:
    print ("Trouble in getting values")
    sys.exit(1)
else:
    trackDiv = trackDiv[0]

artistDiv = pageSoup.findAll("a", {"class": "nowPlayingTopInfo__current__artistName"})[0]
albumDiv = pageSoup.findAll("a", {"class": "nowPlayingTopInfo__current__albumName"})[0]
elapsedDiv = pageSoup.findAll("span", {"data-qa": "elapsed_time"})[0]
totalDiv = pageSoup.findAll("span", {"data-qa": "remaining_time"})[0]
playButton = pageSoup.findAll("button", {"aria-label": "Play"})
play_status = ""
if playButton:
    if playButton[0]['data-qa'] == "pause_button":
        play_status="Playing"
    elif playButton[0]['data-qa'] == "play_button":
        play_status="Paused"
thumbsUpButton = pageSoup.find("button", {"data-qa": "thumbs_up_button"})
thumbsUpStatus = "Unknown"
if thumbsUpButton:
    if "aria-checked" in thumbsUpButton.attrs:
        if thumbsUpButton.attrs['aria-checked'] == 'true':
            thumbsUpStatus = "Yes"
        elif thumbsUpButton.attrs['aria-checked'] == 'false':
            thumbsUpStatus = "No"

title = trackDiv.get_text()
artist = artistDiv.get_text()
album = albumDiv.get_text()
elapsed = elapsedDiv.get_text()
total = totalDiv.get_text()

print ('''\
Pandora Song Info
-----------------
Title:        {}
Artist:       {}
Album:        {}
Elapsed:      {}
Total:        {}
Playing:      {}
ThumbsUp:     {}'''.format(title, artist, album, elapsed, total, play_status, thumbsUpStatus))
