# Repository having scripts that I run in mac

My apple-script collection.

I play music off chrome from mostly
* [pandora](https://www.pandora.com/)
* [saavn](https://www.saavn.com)
* [spotify](https://open.spotify.com)
* [youtube](https://www.youtube.com)

I need a global hotkey to stop/pause music playing. I use quicksilver
to setup the global hotkey. But quicksilver needs a applicatio to
associate a hotkey to. So, I have a simple apple-script based application
that just pauses/plays from the first tab running any of the above.

In addition there are scripts to skip a track, thumbs up/down a track
when I am playing off the radio modes.

There is another script that parses the current page and prints the
current playing song-info.

Since applescript is cumbersome to parse and stuff, I have a python
wrapper that just executes the chosen js commands and extract the page
info, which is later parsed in python.
