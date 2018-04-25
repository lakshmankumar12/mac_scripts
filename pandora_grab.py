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

trackDiv = soup.findAll("a", {"class": "nowPlayingTopInfo__current__trackName"})[0]
artistDiv = soup.findAll("a", {"class": "nowPlayingTopInfo__current__artistName"})[0]
albumDiv = soup.findAll("a", {"class": "nowPlayingTopInfo__current__albumName"})[0]
elapsedDiv = soup.findAll("span", {"data-qa": "elapsed_time"})[0]
totalDiv = soup.findAll("span", {"data-qa": "remaining_time"})[0]
playButton = soup.findAll("button", {"aria-label": "Play"})
play_status = ""
if playButton:
    if playButton[0]['data-qa'] == "pause_button":
        play_status="Playing"
    elif playButton[0]['data-qa'] == "play_button":
        play_status="Paused"

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
Playing:      {}'''.format(title, artist, album, elapsed, total, play_status))
