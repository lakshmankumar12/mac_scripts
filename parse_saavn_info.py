#!/usr/bin/env python3

from __future__ import print_function
import fileinput
import bs4
import mac_script_helper
import sys
import json
from time import sleep
from html import unescape

bwsrTab = mac_script_helper.BrowserTab('https://www.saavn.com')

js = [ '''execute javascript "var title = document.querySelector('#player-album-name')"''',
       '''execute javascript "var aElem = title.querySelector('a')"''',
       '''execute javascript "aElem.click()"''',
     ]

err,page,_ = bwsrTab.sendCommands(js)
if err != 0:
    print ("Trouble in getting page-info from saavn")
    sys.exit(1)

js = [
      mac_script_helper.SaveDocCmd,
     ]

songInfo = None
attempt = 0
while attempt <= 3:
    attempt += 1

    err,page,_ = bwsrTab.sendCommands(js)
    if err != 0:
        print ("Trouble in getting page-info from saavn")
        sys.exit(1)

    pageSoup = bs4.BeautifulSoup(page, 'html.parser')
    with open ('/tmp/a.html','w') as fd:
        fd.write(pageSoup.prettify())

    currAlbFromBottomPlayer = pageSoup.find('span', {"id": "player-album-name"})
    if not currAlbFromBottomPlayer:
        print ("Trouble in getting player-album-name from page .. attempt:{}".format(attempt))
        sleep(0.5*attempt)
        continue

    metainfo = pageSoup.find("div", {"class": "meta-info"})
    if not metainfo:
        print ("Trouble in getting meta-info from page .. attempt:{}".format(attempt))
        sleep(0.5*attempt)
        continue

    pageTitle = metainfo.find("h1", {"class": "page-title"})
    if not pageTitle:
        print ("Trouble in getting page-title from page .. attempt:{}".format(attempt))
        sleep(0.5*attempt)
        continue

    if pageTitle.get_text().strip() != currAlbFromBottomPlayer.get_text().strip():
        print ("Mismatch page info: bottom:{}, top:{} .. attempt:{}".format(unescape(botText), unescape(songInfo['title']), attempt))
        sleep(0.5*attempt)
        continue

    currSong = pageSoup.find("li", {"class": "current-song"})
    if not currSong:
        print ("Trouble in getting current-song from page .. attempt:{}".format(attempt))
        sleep(0.5*attempt)
        continue

    songInfo = currSong.find("div", {"class": "song-json"})
    if not currSong:
        print ("Trouble in getting song-json from page .. attempt:{}".format(attempt))
        sleep(0.5*attempt)
        continue

    songInfo_jsonStr = songInfo.get_text()
    songInfo = json.loads(songInfo_jsonStr)

    break;

if (attempt > 3):
    print ("Too many attempts!")
    sys.exit(1)

elapsedSoup = pageSoup.find('span', {"id": "track-elapsed"})
if not elapsedSoup:
    print ("Trouble in getting track-elapsed from page")
    sys.exit(1)
totalSoup = pageSoup.find('span', {"id": "track-time"})
if not totalSoup:
    print ("Trouble in getting track-time from page")
    sys.exit(1)

title = unescape(songInfo['title'])
artist = unescape(songInfo['singers'])
album = unescape(songInfo['album'])
elapsed = elapsedSoup.get_text()
total = totalSoup.get_text()
year = songInfo['year']

print (
'''Saavn Song Info
---------------
Title:   {}
Artist:  {}
Album:   {}
Elapsed: {}
Total:   {}
Year:    {}'''.format(title, artist, album, elapsed, total, year))
