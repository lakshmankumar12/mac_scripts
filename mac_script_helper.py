#!/usr/bin/env python3

import subprocess
import argparse
import bs4

SaveDocCmd = 'set resultStr to (execute javascript "var h = document.documentElement.innerHTML; h;")'
SetUrlCmdStr = 'set resultStr to (execute javascript "this.document.location = \'{}\'")'
GetUrlCmdStr = 'set resultStr to (execute javascript "this.document.location.href")'

PreCommands='''
set resultStr to ""
tell application "Google Chrome"
    set targetUrl to "{}"
    repeat with w in windows
        repeat with t in tabs of w
            if ((URL of t) starts with targetUrl) then
                tell t
'''

PostCommands='''
                    return resultStr
                end tell
            end if
        end repeat
    end repeat
end tell
return resultStr
'''

class BrowserTab:
    def __init__(self, urlToFind):
        self.pre = PreCommands.format(urlToFind)
        self.post = PostCommands

    def sendCommands(self, commands, debug=False):
        if not isinstance(commands, (list, tuple)):
            commands = [commands]
        cmds = self.pre + '\n' + '\n'.join(commands) + '\n' + self.post
        if debug:
            print ("Sending:\n{}".format(cmds))
        a=subprocess.Popen(["osascript","-"],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        output,err=a.communicate(input=cmds)
        errcode = a.wait()
        return (errcode,output,err)

def execJsCmd(cmd):
    cmd='''
        execute javascript "{}"
    '''.format(cmd)
    cmd = cmd.strip()
    return cmd

def test_page_download(url):
    a = BrowserTab(url)
    js = [
          SaveDocCmd,
         ]
    err,page,_ = a.sendCommands(js)
    if err == 0:
        pageSoup = bs4.BeautifulSoup(page, 'html.parser')
        with open ('/tmp/a.html','w') as fd:
            fd.write(pageSoup.prettify())

def set_url(orig_url, set_url):
    a = BrowserTab(orig_url)
    urlCmd = SetUrlCmdStr.format(set_url)
    js = [ urlCmd ]
    err,page,_ = a.sendCommands(js)
    if err == 0:
        print ("Url set")
    else:
        print ("Some problem..")

def get_url(url):
    a = BrowserTab(url)
    js = [ GetUrlCmdStr ]
    err,page,_ = a.sendCommands(js)
    if err == 0:
        print (page.strip())
    else:
        print ("Some problem..")

if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--set-url", help="url to set")
    parser.add_argument("-g", "--get-url", help="url to set", action="store_true")
    parser.add_argument("--url", help="page to match, default is to download, default url is spotify", default="https://open.spotify.com")

    cmd_options = parser.parse_args()

    if cmd_options.get_url:
        get_url(cmd_options.url)
    elif cmd_options.set_url:
        set_url(cmd_options.url, cmd_options.set_url)
    else:
        test_page_download(cmd_options.url)
