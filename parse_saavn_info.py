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

js = [ '''execute javascript "var title = document.querySelector('#player-track-name')"''',
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

    currSongFromBottomPlayer = pageSoup.find('strong', {"id": "player-track-name"})
    if not currSongFromBottomPlayer:
        print ("Trouble in getting player-track-name from page .. attempt:{}".format(attempt))
        sleep(0.5*attempt)
        continue

    metainfo = pageSoup.findAll("div", {"class": "meta-info"})
    if not metainfo:
        print ("Trouble in getting meta-info from page .. attempt:{}".format(attempt))
        sleep(0.5*attempt)
        continue

    metainfo = metainfo[0]
    songInfo = metainfo.findAll("div", {"class": "song-json"})
    if not songInfo:
        print ("Trouble in getting song-json from page .. attempt:{}".format(attempt))
        sleep(0.5*attempt)
        continue

    songInfo_jsonStr = songInfo[0].get_text()
    songInfo = json.loads(songInfo_jsonStr)

    botText = currSongFromBottomPlayer.get_text()
    if unescape(botText) != unescape(songInfo['title']):
        print ("Mismatch page info: bottom:{}, top:{} .. attempt:{}".format(unescape(botText), unescape(songInfo['title']), attempt))
        sleep(0.5*attempt)
        continue

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
