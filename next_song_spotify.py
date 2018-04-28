#!/usr/bin/env python3

import mac_script_helper
import sys

bwsrTab = mac_script_helper.BrowserTab('https://open.spotify.com')

js = [
        '''execute javascript "var h = document.querySelector('[title=\\"Next\\"]');"''',
        '''execute javascript "h.click();"'''
     ]

errcode,page,errmsg = bwsrTab.sendCommands(js)
if errcode != 0:
    print ("Trouble in clicking skip in pandora page: code:{} msg:{}".format(errcode, errmsg))
    sys.exit(1)

