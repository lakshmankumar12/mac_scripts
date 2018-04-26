#!/usr/local/bin/python3

from __future__ import print_function
import fileinput
import bs4
import mac_script_helper
import sys
import json

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
attempt = 1
while attempt <= 3:
    err,page,_ = bwsrTab.sendCommands(js)
    if err != 0:
        print ("Trouble in getting page-info from saavn")
        sys.exit(1)

    pageSoup = bs4.BeautifulSoup(page, 'html.parser')
    metainfo = pageSoup.findAll("div", {"class": "meta-info"})

    with open ('/tmp/a.html','w') as fd:
        fd.write(pageSoup.prettify())

    if not metainfo:
        print ("Trouble in getting meta-info from page")
        sys.exit(1)
    metainfo = metainfo[0]
    songInfo = metainfo.findAll("div", {"class": "song-json"})
    if not songInfo:
        print ("Trouble in getting song-json from page .. attempt:{}".format(attempt))
        if (attempt <= 3):
            attempt += 1
            continue
        sys.exit(1)
    songInfo_jsonStr = songInfo[0].get_text()
    songInfo = json.loads(songInfo_jsonStr)
    break;

elapsedSoup = pageSoup.find('span', {"id": "track-elapsed"})
if not elapsedSoup:
    print ("Trouble in getting track-elapsed from page")
    sys.exit(1)
totalSoup = pageSoup.find('span', {"id": "track-time"})
if not totalSoup:
    print ("Trouble in getting track-time from page")
    sys.exit(1)

title = songInfo['title']
artist = songInfo['singers']
album = songInfo['album']
elapsed = elapsedSoup.get_text()
total = totalSoup.get_text()
year = songInfo['year']

print (
'''Saavn Song Info
---------------
Title:        {}
Artist:       {}
Album:        {}
Elapsed:      {}
Total:        {}
Year:         {}'''.format(title, artist, album, elapsed, total, year))
