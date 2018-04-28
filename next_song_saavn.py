#!/usr/bin/env python3

import mac_script_helper
import sys

bwsrTab = mac_script_helper.BrowserTab('https://www.saavn.com')

js = [
        '''execute javascript "var h = document.querySelector('#fwd');"''',
        '''execute javascript "h.click()"'''
     ]

errcode,page,errmsg = bwsrTab.sendCommands(js)
if errcode != 0:
    print ("Trouble in clicking skip in pandora page: code:{} msg:{}".format(errcode, errmsg))
    sys.exit(1)

