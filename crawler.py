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

docDB={}
#mysql connector
db = MySQLdb.connect(host="localhost", # your host, usually localhost
		     user="root", # your username
		      passwd="test", # your password
		      db="storage") # name of the data base
cur = db.cursor()
#cur.execute('SHOW DATABASES LIKE "storage";')
cur.execute('SHOW TABLES;')
db.commit()
print "checking database"
if len(cur.fetchall())==0: #database doesn't exist, needs to be created
	print "db doesn't exist, creating one"
	cur.execute( "create table docs ("+
		     "docID VARCHAR(100) NOT NULL PRIMARY KEY,"+
		     "title VARCHAR(100),"+
		     "html TEXT,"+
		     "lastmodified TIMESTAMP(6) );"
		     );
	db.commit()
	cur.execute('SHOW DATABASES LIKE "storage";')
	db.commit()
	assert len(cur.fetchall())!=0, 'database fail to create'



class doc(object):
	def __init__(self, docID, title, html):
		self.docID = docID
		self.title = title
		self.html = html
	def setHTML(self, html): #gets the entire HTML doc
		self.html = html
	def getHTML(self):
		return self.html
	def getTitle(self):
		return self.title
	def getURL(self):
		return self.url	
	def getDocID(self):
		return self.docID

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
	#elif re110G.match(' ', unicode(element)):
	#	return False
	return True

def crawl():
	seedURL = ['http://www.cs.sfu.ca/people/faculty.html']
	parsedURL = []
	while len(seedURL)!=0:
		url = seedURL.pop(0) #gets first element
		if (url in parsedURL):
			print 'URL {0} has been visited'.format(url)
			continue
		else:
			parsedURL.append(url)
		print 'Reading URL %s', url
		print 'Parsing seed URL'
		html = urllib2.urlopen(url)
		soup = BeautifulSoup(html)
			
		tempList = extractInternalLinks(soup)	
		#seedURL = seedURL + tempList
				

		pageTitle = clean(soup.title.string)
		#docID = randint(10, 9999999) #random id for docID
		docID = url
		docObj = doc(docID, pageTitle, html)
	
		#if docID not in docDB:#check if doc ID is unique
		#	docDB[docID]=docObj
		#else:
		#	docID = randint(9999999,9999999999)#pick something else
		#	docDB[docID]=docObj	
		#docDB[docID].setHTML(soup)
		sql = 'insert into docs (docID, title, html) values ("%s", "%s", "%s");'
		cur.execute(sql, (docID, pageTitle, soup) )
	
		
		#print clean(docDB[docID].getTitle())
		#print docDB[docID].getHTML()
		try:
			db.commit()
		except:
			print 'duplicates. check sql'
		#text = soup.findAll(text=True)
		#page = filter(visible, text)
		#print page
		seedURL = seedURL + tempList

def extractInternalLinks(parentSoup):
	links=[]

	for link in parentSoup.find_all('a'):
		link = link.get('href')
		try:
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
			
			relevance = checkRelevance(page)
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

def checkRelevance(page):
	threshold = 10;
	#15 keywords
	keyWords = ['grad',
			'graduate',
			'students',
			'student',
			'research',
			'teaching',
			'contact',
			'degrees',
			'degree',
			'supervised',
			'supervise',
			'publications',
			'publication',
			'current research',
			'graduate students',
			'graduate student',
			'selected publications',
			'ph.d',
			'm.sc.']
	count = 0
	for token in keyWords:		
		if token in page:		
			count=count+1
	temp = float(100)*float((float(count)/float(len(keyWords))))	
	
	if temp>threshold:
		return True 
	else:
		return False 

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
	print checkRelevance(page)
#test()


if __name__ == "__main__":
	crawl()
