#!/usr/bin/python

from __future__ import print_function
import fileinput
import bs4


all_of_stdin = ""

for line in fileinput.input():   #this one will pick stdin or if some arg(s) is/are given, it will open that as a file!
    all_of_stdin += line

souped_content = bs4.BeautifulSoup(all_of_stdin,'html.parser')

print (souped_content.prettify().encode('utf-8'))

