from bs4 import BeautifulSoup
from collections import Counter 
from random import randint
import codecs
import locale
import sys
import pdb
import os
import re
import urllib2
import MySQLdb
import rel

from doc import doc

def visible(element):
	if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
		return False
	elif re.match('<!--.*-->', unicode(element)):
		return False
	elif re.match('\n', unicode(element)):
		return False
	#elif re110G.match(' ', unicode(element)):
	#	return False
	return True

html = urllib2.urlopen('http://www.cs.sfu.ca/people/faculty.html')
soup = BeautifulSoup(html)
text = soup.findAll(text=True)
page = filter(visible, text)
page = [token.strip(' ').lower() for token in page]
print rel.check(page)

a = doc('111','hello','<had')
print a.getHTML()



