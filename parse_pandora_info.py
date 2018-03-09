#!/usr/bin/python

from __future__ import print_function
import fileinput
import bs4


## Sample Input
##     <div class="Marquee Marquee--stopOnHover"><div class="Marquee__wrapper__content">Requiem For A Dream</div></div>`Jennifer Thomas`Illumination`2:22`3:34`Playing

for line in fileinput.input():   #this one will pick stdin or if some arg(s) is/are given, it will open that as a file!
    (title,artist,album,elapsed,total,playing) = line.split("`")

title_bs4 = bs4.BeautifulSoup(title,'html.parser')
print ('''\
Pandora Song Info
-----------------
Title:   {}
Artist:  {}
Album:   {}
Elapsed: {}
Total:   {}
Playing: {}'''.format(title_bs4('div')[0].get_text(), artist, album, elapsed, total, playing))
