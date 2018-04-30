#!/usr/bin/env python3

import mac_script_helper
import sys

bwsrTab = mac_script_helper.BrowserTab('https://www.saavn.com')

js = [
        '''execute javascript "var h = document.querySelector('#fwd');"''',
        '''execute javascript "h.click()"''',
        '''set resultStr to "Saavn clicked"'''
     ]

errcode,page,errmsg = bwsrTab.sendCommands(js)
if errcode != 0:
    print ("Trouble in clicking skip in saavn page: code:{} msg:{}".format(errcode, errmsg))
    sys.exit(1)

if page.strip() == "Saavn clicked":
    print ("fwd in saavn clicked")
    sys.exit(0)

bwsrTab = mac_script_helper.BrowserTab('https://www.pandora.com/')

js = [
        '''execute javascript "var h = document.querySelector('[data-qa=\\"skip_button\\"]');"''',
        '''execute javascript "h.click()"''',
        '''set resultStr to "pandora clicked"''',
     ]

errcode,page,errmsg = bwsrTab.sendCommands(js)
if errcode != 0:
    print ("Trouble in clicking skip in pandora page: code:{} msg:{}".format(errcode, errmsg))
    sys.exit(1)

if page.strip() == "pandora clicked":
    print ("pandora skip_button clicked")
    sys.exit(0)


bwsrTab = mac_script_helper.BrowserTab('https://open.spotify.com')

js = [
        '''execute javascript "var h = document.querySelector('[title=\\"Next\\"]');"''',
        '''execute javascript "h.click();"''',
        '''set resultStr to "Spotify clicked"'''
     ]

errcode,page,errmsg = bwsrTab.sendCommands(js)
if errcode != 0:
    print ("Trouble in clicking skip in pandora page: code:{} msg:{}".format(errcode, errmsg))
    sys.exit(1)

if page.strip() == "Spotify clicked":
    print ("Spotify next clicked")
    sys.exit(0)
