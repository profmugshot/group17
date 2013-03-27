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
import rel #relevance check
from doc import doc #doc obj
from urlparse import urljoin
from sets import Set
import itertools


##########db connection############
docDB={}
#mysql connector
db = MySQLdb.connect(host="localhost", # your host, usually localhost
		     user="root", # your username
		      passwd="test", # your password
		      db="storage") # name of the data base
cur = db.cursor()
cur.execute('SHOW TABLES;')
db.commit()
print "checking database"
if len(cur.fetchall())==0: #database doesn't exist, needs to be created
	print "db doesn't exist, creating one"
	cur.execute( "create table docs ("+
		     "docID VARCHAR(100) NOT NULL PRIMARY KEY,"+
		     "title VARCHAR(100),"+
		     "html LONGTEXT,"+
		     "lastmodified TIMESTAMP(6) );"
		     );
	db.commit()
	cur.execute('SHOW DATABASES LIKE "storage";')
	db.commit()
	assert len(cur.fetchall())!=0, 'database fail to create'

	#this is to filter out the main cs.sfu.ca page. Reduces internal links parsing
	sql = 'insert into docs (docID, title, html) values ("%s", "%s", "%s");'
	cur.execute(sql, ('http://www.cs.sfu.ca/', 'main cs sfu page', 'Nill') )
	db.commit()
######end db connection########



#clean up formatting for web page title
#gets rid of newlines and extra spaces
def clean(string):
	return " ".join(string.split())

def visible(element):
	if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
		return False
	elif re.match('<!--.*-->', unicode(element)):
		return False
	elif re.match('\n', unicode(element)):
		return False
	return True

def crawl():
	seedURL = ['http://www.cs.sfu.ca/people/faculty.html']
	parsedURL = []
	while len(seedURL)!=0:
		print '###### start iterate ######'
		url = seedURL.pop(0) #gets first element
		parsedURL.append(url)
		print 'Reading URL %s', url
		print 'Parsing seed URL'
		html = urllib2.urlopen(url)
		soup = BeautifulSoup(html)
			
		extractedLinks = extractInternalLinks(url, soup)	

		pageTitle = clean(soup.title.string)

		docID = url
		docObj = doc(docID, pageTitle, html)

		try:
			sql = 'insert into docs (docID, title, html) values ("%s", "%s", "%s");'
			cur.execute(sql, (docID, pageTitle, soup) )
		except:
			print 'duplicate entries'
		try:
			db.commit()
		except:
			print 'duplicates. check sql'
		parsedSet= Set(parsedURL)
		seedSet = Set(seedURL)
		tempSet = Set(extractedLinks)
		
		#get all urls in tempSet that is not in parsedSet (tempSet - parsedSet)
		toBeAddedURL = tempSet.difference(parsedSet) 
		
		seedSet = seedSet.union(toBeAddedURL)
		seedURL = list(seedSet)
		print 'length of seed URL ', len(seedURL)
		print 'length of parsedURL ', len(list(tempSet))
		
		print '#####ending iteration####'

def extractInternalLinks(seedURL, parentSoup):
	links=[]

	for link in parentSoup.find_all('a'):
		link = link.get('href')
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
			page = [token.split(' ') for token in page]
			page = list(itertools.chain.from_iterable(page))
			page = [re.sub(',*:*;*-*', '', token) for token in page]
			relevance = rel.check(page)
			#print "Page with URL {0} is {1}.".format(link, "relevant" if relevance else "not relevant")
			if relevance:
				links.append(link)
		except:
			print 'empty link'
	return links


#ignore for now
#can be used later for index generation
def freqCount():
	print 'stuff'
	freqList = Counter(linksList)
	freqList = sorted(freqList.items(), key=lambda x: x[1], reverse=True)
	sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
	#for token in freqList:
	#	print token[0], token[1]
	x = [token[0] in t for token in freqList]
	y = [token[1] in t for token in freqList]
#	print x

#debugging use, indivdually check page relevance
def test():
	#html = urllib2.urlopen('http://www.cs.sfu.ca/~ggbaker/')
	html = urllib2.urlopen('http://www.cs.sfu.ca/~woshun/')
	soup = BeautifulSoup(html)
	text = soup.findAll(text=True)
	page = filter(visible, text)
	page = [token.strip(' ').lower() for token in page]
	print page
	print rel.check(page)
#test()


if __name__ == "__main__":
	crawl()
