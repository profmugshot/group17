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
import rel
import itertools
from doc import doc
from urlparse import urljoin

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
def test():
	html = urllib2.urlopen('http://www.cs.sfu.ca/people/faculty.html')
	soup = BeautifulSoup(html)
	text = soup.findAll(text=True)
	page = filter(visible, text)
	page = [token.strip(' ').lower() for token in page]
	print rel.check(page)

	a = doc('111','hello','<had')
	print a.getHTML()

def extractInternalLinks(seedURL, parentSoup):
	links=[]

	for link in parentSoup.find_all('a'):
		link = link.get('href')
		print link
		try:
			link = urljoin(seedURL, link)
			if not('cs.sfu.ca' in link.lower()):
				continue
			try:
				html = urllib2.urlopen(link) #pulls html
				parsedPage = BeautifulSoup(html)
			except:
				print 'cant open page' + link 
				continue
		
			text = parsedPage.findAll(text=True)
			page = filter(visible, text)
			page = [token.strip(' ').lower() for token in page]
			
			relevance = rel.check(page)
			print "Page with URL {0} is {1}.".format(link, "relevant" if relevance else "not relevant")
			if relevance:
				links.append(link)
		except:
			print 'empty link'
			
		#	if link.startswith('/'): #deals with internal links eg: /people/faculty.html
		#		link = 'http://www.cs.sfu.ca'+link.get('href')
		#		links.append(link)
		#	elif 'cs.sfu.ca' in link:
		#		links.append(link)
	return links

def linkformat():
	url = 'http://www.cs.sfu.ca/~kabanets/'
	html = urllib2.urlopen('http://www.cs.sfu.ca/~kabanets/')
	soup = BeautifulSoup(html)
	tempList = extractInternalLinks(url, soup)	
	print tempList

#linkformat()

def relevtest():
	url = 'http://www.cs.sfu.ca/~kabanets/pubs.html'
	html = urllib2.urlopen(url)
	soup = BeautifulSoup(html)

	text = soup.findAll(text=True)
	page = filter(visible, text)
	
	page = [token.strip(' ').lower() for token in page]
	page = [token.split(' ') for token in page]
	page = list(itertools.chain.from_iterable(page))
	page = [re.sub(',*:*;*-*', '', token) for token in page]
	relevance = rel.check(page)
	print relevance
relevtest()
