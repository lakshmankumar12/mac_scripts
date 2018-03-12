#!/usr/bin/python

from __future__ import print_function
import fileinput
import bs4


## Sample Input
##     <div class="Marquee Marquee--stopOnHover"><div class="Marquee__wrapper__content">Requiem For A Dream</div></div>`Jennifer Thomas`Illumination`2:22`3:34`Playing
##  or
##     <div class="Marquee Marquee--stopOnHover"><div class="Marquee__hiddenSizer">Apologize (Feat. OneRepublic)</div><div class="Marquee__wrapper"><div class="Marquee__wrapper__content--animating" style="animation-duration: 5s;"><div class="Marquee__wrapper__content__child">Apologize (Feat. OneRepublic)</div><div class="Marquee__wrapper__content__child">Apologize (Feat. OneRepublic)</div></div></div></div>

for line in fileinput.input():   #this one will pick stdin or if some arg(s) is/are given, it will open that as a file!
    (title,artist,album,elapsed,total,playing) = line.split("`")

title_bs4 = bs4.BeautifulSoup(title,'html.parser')
extracted_title = title_bs4.findAll("div", {"class": "Marquee__wrapper__content"})
if not extracted_title:
    extracted_title = title_bs4.findAll("div", {"class": "Marquee__wrapper__content__child"})
if not extracted_title:
    # huh!
    extracted_title = title_bs4('div')

extracted_title = extracted_title[0].get_text()


print ('''\
Pandora Song Info
-----------------
Title:   {}
Artist:  {}
Album:   {}
Elapsed: {}
Total:   {}
Playing: {}'''.format(extracted_title, artist, album, elapsed, total, playing))

