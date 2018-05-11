#!/usr/bin/env python3

import mac_script_helper
import bs4
import sys
import re



def getPandoraNowPlayingPage(bwsrTab):
    js = [
           '''execute javascript "var now_playing = document.querySelector('[data-qa=\\"header_now_playing_link\\"]'); now_playing.click();"'''
         ]

    err,page,_ = bwsrTab.sendCommands(js)
    if err != 0:
        print ("Trouble in getting page-info from pandora")
        sys.exit(1)

    attempt = 0
    pageSoup = None
    trackDiv = None
    artistDiv = None
    albumDiv = None
    while attempt <= 3:
        attempt += 1
        js = [
              mac_script_helper.SaveDocCmd,
             ]

        err,page,_ = bwsrTab.sendCommands(js)
        if err != 0:
            print ("Trouble in getting page-info from pandora")
            sys.exit(1)

        pageSoup = bs4.BeautifulSoup(page, 'html.parser')
        with open ('/tmp/a.html','w') as fd:
            fd.write(pageSoup.prettify())

        trackDivParent = pageSoup.find("a", {"class": "nowPlayingTopInfo__current__trackName"})
        if not trackDivParent:
            print ("Trouble in getting now-playing track info .. attempt:{}".format(attempt))
            continue

        artistDiv = pageSoup.findAll("a", {"class": "nowPlayingTopInfo__current__artistName"})[0]
        albumDiv = pageSoup.findAll("a", {"class": "nowPlayingTopInfo__current__albumName"})[0]
        break

    if attempt > 3:
        print ("Too many attempts:{}".format(attempt))
        return None

    return pageSoup

def getPandoraNowPlayingDetails(bwsrTab, pageSoup):

    trackDiv = None
    trackDivParent = pageSoup.find("a", {"class": "nowPlayingTopInfo__current__trackName"})
    trackDiv = trackDivParent.find("div", {"class": "Marquee__wrapper__content"})
    if not trackDiv:
        trackDiv = trackDivParent.find("div", {"class": "Marquee__wrapper__content__child"})
        if not trackDiv:
            trackDiv = trackDivParent
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

    artUrl=""
    artDiv=pageSoup.find("div", {"data-qa" :"album_active_image"})
    if artDiv:
        if 'style' in artDiv.attrs:
            value = artDiv.attrs['style']
            matches = re.findall(r'\"(.+?)\"',value)
            if matches:
                artUrl = matches[0]

    title = trackDiv.get_text()
    artist = artistDiv.get_text()
    album = albumDiv.get_text()
    elapsed = elapsedDiv.get_text()
    total = totalDiv.get_text()

    return (title, artist, album, elapsed, total, play_status, thumbsUpStatus, artUrl)


def getPandoraAlbumPage(bwsrTab, album):
    attempt = 0
    year = ""
    tracksInAlb = []
    discography  = []
    while attempt <= 3:
        attempt += 1

        js = [
               '''execute javascript "var albumClick = document.querySelector('.nowPlayingTopInfo__current__albumName'); albumClick.click();"'''
             ]

        err,page,_ = bwsrTab.sendCommands(js)
        if err != 0:
            print ("Trouble in getting page-info from pandora")
            sys.exit(1)

        js = [
              mac_script_helper.SaveDocCmd,
             ]

        err,page,errInfo = bwsrTab.sendCommands(js)
        if err != 0:
            print ("Trouble in getting page-info from album page")
            sys.exit(1)

        pageSoup = bs4.BeautifulSoup(page, 'html.parser')
        with open ('/tmp/b.html','w') as fd:
            fd.write(pageSoup.prettify())

        allAlbums = pageSoup.findAll("div", {"class": ["BackstageGridItem","BackstageGridItem--expanded"]})
        if not allAlbums:
            print ("Yet to load page fully .. attempt : {}".format(attempt))
            continue

        discography = []
        for albDiv in allAlbums:
            first = albDiv.find("a", {"class": "BackstageGridItem__text__first"})
            yearDiv = albDiv.find("a", {"class": "BackstageGridItem__text__second"})
            alb = first.get_text().strip()
            yr  = yearDiv.get_text().strip()
            discography.append((alb,yr))
            if alb == album:
                year = yearDiv.get_text()

        allTracks = pageSoup.findAll("div", {"data-qa": "backstage_album_track"})
        for trackDiv in allTracks:
            titDiv = trackDiv.find("a")
            durDiv = trackDiv.find("div", {"class": "BackstageAlbumTrack__trackDuration"})
            tracksInAlb.append((titDiv.get_text().strip(), durDiv.get_text().strip()))

        break

    return (year, discography, tracksInAlb)

OutputFormatString = '''\
Pandora Song Info
-----------------
Title:        {}
Artist:       {}
Album:        {}
Elapsed:      {}
Total:        {}
Playing:      {}
Year:         {}
ArtUrl:       {}
ThumbsUp:     {}'''

def main():
    bwsrTab = mac_script_helper.BrowserTab('https://www.pandora.com/')
    pageSoup = getPandoraNowPlayingPage(bwsrTab)
    if not pageSoup:
        sys.exit(1)
    (title, artist, album, elapsed, total, play_status, thumbsUpStatus, artUrl)  = getPandoraNowPlayingDetails(bwsrTab, pageSoup)
    (year, discography, tracksInAlb)  = getPandoraAlbumPage(bwsrTab, album)

    if discography:
        print("Discography")
        print("-----------")
        for n,(a,y) in enumerate(discography,1):
            print ("{}. {}  {}".format(n,y,a))

    if tracksInAlb:
        print("Other songs in alb")
        print("------------------")
        for n,(t,d) in enumerate(tracksInAlb,1):
            print("{}. {}  {}".format(n,d,t))

    print (OutputFormatString.format(title, artist, album, elapsed, total, play_status, year, artUrl, thumbsUpStatus))

if __name__ == "__main__":
    main()
