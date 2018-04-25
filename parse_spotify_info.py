#!/usr/bin/python3

from __future__ import print_function
import fileinput
import bs4
import re
import sys
import pdb


orig_prettify = bs4.BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)
def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))
bs4.BeautifulSoup.prettify = prettify

bs4parser="html.parser"

with open(sys.argv[1],'r') as fd:
    soup = bs4.BeautifulSoup(fd,bs4parser)

with open(sys.argv[2],'w') as fd:
    fd.write(soup.prettify())

trackInfo = soup.findAll("div", {"class": "track-info"})[0]
albumInfo1 = soup.findAll("div", {"class": "media-bd"})
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
progress = soup.findAll("div", {"class": "playback-bar__progress-time"})

pause_btn = soup.findAll("button", {"title": "Pause"})
if not pause_btn:
    play_btn = soup.findAll("button", {"title": "Play"})
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
Pandora Song Info
-----------------
Title:        {}
Artist:       {}
Album:        {}
Album-artist: {}
Year:         {}
Elapsed:      {}
Total:        {}
Playing:      {}'''.format(title, artist, album, albumArtist, year, elapsed, total, play_status))
