import subprocess

SaveDocCmd = 'set doc to (execute javascript "var h = document.documentElement.innerHTML; h;")'

PreCommands='''
set doc to ""
tell application "Google Chrome"
    set found_tab to false
    set targetUrl to "{}"
    set window_list to every window
    repeat with the_window in window_list
        if found_tab is equal to true then
            exit repeat
        end if
        set tab_list to every tab in the_window
        repeat with the_tab in tab_list
            if ((URL of the_tab) contains targetUrl) then
                tell the_tab
'''

PostCommands='''
                end tell
                set found_tab to true
                exit repeat
            end if
        end repeat
    end repeat
end tell
return doc
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

def test_group_of_js():
    a = BrowserTab('https://open.spotify.com')
    js = [
          #'''execute javascript "var h = document.querySelector('[title=\\"Pause\\"]');"''',
          #'''execute javascript "if(h == null) var h = document.querySelector('[title=\\"Play\\"]');"''',
          #'''execute javascript "h.click()"''',
          SaveDocCmd,
         ]
    err,page,_ = a.sendCommands(js)
    if err == 0:
        with open ('/tmp/a.html','w') as fd:
            fd.write(page)

if __name__ == "__main__":
    test_group_of_js()