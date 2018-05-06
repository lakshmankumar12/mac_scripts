#!/usr/bin/env python3

import mac_script_helper
import bs4
import sys
from time import sleep
from html import unescape
import json
import datetime
from daemonize import Daemonize
import signal



pandScrobbleFileName='/Users/lakshman.narayanan/Downloads/songs-download/English/pandoraScrobble.txt'
saavnScrobbleFileName='/Users/lakshman.narayanan/Downloads/songs-download/saavn/saavnScrobble.txt'
scrobbleDebugFileName='/tmp/pandsaavnScrob.html'
scrobbleErrFileName='/tmp/pandsaavnScrob.err.txt'
datetimeformat='%Y-%m-%d-%H-%M-%S'
scrobblePidFile='/tmp/pandsaavnScrob.pid'


def getPandoraTitleAlbum(errFile, pageDebugFileName):
    bwsrTab = mac_script_helper.BrowserTab('https://www.pandora.com/')
    js = [
           '''execute javascript "var now_playing = document.querySelector('[data-qa=\\"header_now_playing_link\\"]'); now_playing.click();"'''
         ]

    err,page,_ = bwsrTab.sendCommands(js)
    if err != 0:
        print ("Trouble in getting page-info from pandora", file=errFile)
        return (None,None,None)

    js = [
          mac_script_helper.SaveDocCmd,
         ]

    err,page,_ = bwsrTab.sendCommands(js)
    if err != 0:
        print ("Trouble in getting page-info from pandora", file=errFile)
        return (None,None,None)

    if len(page.strip()) == 0:
        print ("No pandora page", file=errFile)
        return (None, -1, None)

    pageSoup = bs4.BeautifulSoup(page, 'html.parser')
    with open (pageDebugFileName,'w') as fd:
        fd.write(pageSoup.prettify())

    trackDiv = pageSoup.find("a", {"class": "nowPlayingTopInfo__current__trackName"})
    if not trackDiv:
        print ("Trouble in getting values", file=errFile)
        return (None,None,None)

    artistDiv = pageSoup.find("a", {"class": "nowPlayingTopInfo__current__artistName"})
    albumDiv = pageSoup.find("a", {"class": "nowPlayingTopInfo__current__albumName"})

    title = trackDiv.get_text().strip()
    artist = artistDiv.get_text().strip()
    album = albumDiv.get_text().strip()

    return (title, artist, album)

def getLastScrobbledInfo(scrobbleFileName):
    lastLine = None
    try:
        with open(scrobbleFileName,'r') as fd:
            line = None
            for line in fd:
                pass
            lastLine = line
    except FileNotFoundError:
        pass
    if lastLine:
        lastLine = lastLine.strip()
        firstDemar = lastLine.find('`')
        lastLine = lastLine[firstDemar+1:]
    return lastLine


def workOnScrobble(scrobbleErr, scrobbleFileName, toAdd):
    lastScrobbled = getLastScrobbledInfo(scrobbleFileName)
    newline='`'.join(toAdd)
    print ("Got lastScrobbled info as {} and newline is {}".format(lastScrobbled, newline),file=scrobbleErr)
    if lastScrobbled:
        if lastScrobbled == newline:
            return;
    nowStr = datetime.datetime.now().strftime(datetimeformat)
    newline = nowStr + '`' + newline
    print ("Updating {} in {} file".format(newline, scrobbleFileName), file=scrobbleErr)
    newline+='\n'
    with open (scrobbleFileName, 'a') as fd:
        fd.write(newline)

def getSaavnTitleAlbum(errFile, debugFileName):
    bwsrTab = mac_script_helper.BrowserTab('https://www.saavn.com')
    js = [ '''execute javascript "var title = document.querySelector('#player-album-name')"''',
           '''execute javascript "var aElem = title.querySelector('a')"''',
           '''execute javascript "aElem.click()"''',
         ]

    err,page,_ = bwsrTab.sendCommands(js)
    if err != 0:
        print ("Trouble in getting page-info from saavn", file=errFile)
        return (None, None, None)

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
            return (None, None, None)

        pageSoup = bs4.BeautifulSoup(page, 'html.parser')
        with open (debugFileName,'w') as fd:
            fd.write(pageSoup.prettify())

        currAlbFromBottomPlayer = pageSoup.find('span', {"id": "player-album-name"})
        if not currAlbFromBottomPlayer:
            print ("Trouble in getting player-album-name from page .. attempt:{}".format(attempt), file=errFile)
            sleep(0.5*attempt)
            continue

        metainfo = pageSoup.find("div", {"class": "meta-info"})
        if not metainfo:
            print ("Trouble in getting meta-info from page .. attempt:{}".format(attempt), file=errFile)
            sleep(0.5*attempt)
            continue

        pageTitle = metainfo.find("h1", {"class": "page-title"})
        if not pageTitle:
            print ("Trouble in getting page-title from page .. attempt:{}".format(attempt), file=errFile)
            sleep(0.5*attempt)
            continue

        botText = unescape(currAlbFromBottomPlayer.get_text().strip())
        pageTit = unescape(pageTitle.get_text().strip())
        if pageTit != botText:
            print ("Mismatch page info: bottom:{}, top:{} .. attempt:{}".format(botText, pageTit, attempt), file=errFile)
            sleep(0.5*attempt)
            continue

        currSong = pageSoup.find("li", {"class": "current-song"})
        if not currSong:
            print ("Trouble in getting current-song from page .. attempt:{}".format(attempt), file=errFile)
            sleep(0.5*attempt)
            continue

        songInfo = currSong.find("div", {"class": "song-json"})
        if not currSong:
            print ("Trouble in getting song-json from page .. attempt:{}".format(attempt), file=errFile)
            sleep(0.5*attempt)
            continue

        songInfo_jsonStr = songInfo.get_text()
        songInfo = json.loads(songInfo_jsonStr)

        break;

    if (attempt > 3):
        print ("Too many attempts!", file=errFile)
        return (None, None, None)

    title = unescape(songInfo['title'])
    artist = unescape(songInfo['singers'])
    album = unescape(songInfo['album'])
    permaUrl = unescape(songInfo['perma_url'])

    return (title, artist, album, permaUrl)

def scrobble():
    with open (scrobbleErrFileName, 'a') as scrobbleErr:
        print ("Waking up at {}".format(datetime.datetime.now().strftime(datetimeformat)), file=scrobbleErr)
        toAdd = getPandoraTitleAlbum(scrobbleErr, scrobbleDebugFileName)
        if toAdd[0]:
            workOnScrobble(scrobbleErr, pandScrobbleFileName, toAdd)
            return
        elif not toAdd[1]:
            print ("Pandora gave both title and artist empty", file=scrobbleErr)
            return
        toAdd = getSaavnTitleAlbum(scrobbleErr, scrobbleDebugFileName)
        if toAdd[0]:
            workOnScrobble(scrobbleErr, saavnScrobbleFileName, toAdd)

def signal_handler(signal, frame):
    with open (scrobbleErrFileName, 'a') as scrobbleErr:
        print ("Signalled at {}".format(datetime.datetime.now().strftime(datetimeformat)), file=scrobbleErr)
    scrobble()

def main():
    signal.signal(signal.SIGUSR1, signal_handler)
    while True:
        scrobble()
        sleep(60)

daemon = Daemonize(app="pandora-scrobble", pid=scrobblePidFile, action=main)
daemon.start()
