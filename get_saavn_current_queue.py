#!/usr/bin/env python3

from __future__ import print_function
import fileinput
import bs4
import mac_script_helper
import sys
import json
from time import sleep
from html import unescape

def get_current_queue():
    bwsrTab = mac_script_helper.BrowserTab('https://www.saavn.com')
    js = [
          mac_script_helper.SaveDocCmd,
         ]

    attempt = 0
    while attempt <= 3:
        err,page,_ = bwsrTab.sendCommands(js)
        if err != 0:
            print ("Trouble in getting page from saavn .. attempt:{}".format(attempt))
            continue

        pageSoup = bs4.BeautifulSoup(page, 'html.parser')
        with open ('/tmp/a.html','w') as fd:
            fd.write(pageSoup.prettify())

        drawerQueue = pageSoup.find('ol', {"id": "drawer-queue-group"})
        if not drawerQueue:
            print ("Trouble in getting drawer-queue-group from page .. attempt:{}".format(attempt))
            sleep(0.5*attempt)
            continue

        tracks = []
        trackList = drawerQueue.findAll("li", recursive=False)
        for t in trackList:
            title = t.find("h4")
            if not title:
                continue
            album = t.find("h5")
            if not album:
                continue
            track = {}
            track['TIT2'] = title.get_text()
            track['TALB'] = album.get_text()
            tracks.append(track)

        return tracks

    print ("Too many attempts - {}".format(attempt))
    return None

def dumpTracksFromSaavnAsJson(fileName):
    tracks = get_current_queue()
    if not tracks:
        return

    string = json.dumps(tracks, indent=4, sort_keys=True)
    with open (fileName,'w') as fd:
        fd.write(string)

def main():

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("fileToDump",   help="json file to dump")

    cmd_options = parser.parse_args()

    dumpTracksFromSaavnAsJson(cmd_options.fileToDump)

main()
