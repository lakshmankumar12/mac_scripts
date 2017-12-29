#!/usr/bin/python

from __future__ import print_function
import fileinput
import bs4


for line in fileinput.input():   #this one will pick stdin or if some arg(s) is/are given, it will open that as a file!
  (title,album,singers,elapsed,total) = line.split("`")

print ("Saavn Song Info\n----------------")
title_bs4 = bs4.BeautifulSoup(title,'html.parser')
print ("title: {}".format(title_bs4('a')[0].contents[0]))

album_bs4 = bs4.BeautifulSoup(album, 'html.parser')
print ("album: {}".format(album_bs4('a')[0].contents[0]))

singers_bs4 = bs4.BeautifulSoup(singers, 'html.parser')
singers_str = []
for i in singers_bs4('a'):
    singers_str.append(i.contents[0])
print ("singers: {}".format(",".join(singers_str)))
print ("elapsed: {}".format(elapsed))
print ("total: {}".format(total))
