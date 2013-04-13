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
		      passwd="ihave1cookie", # your password
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
	sql = 'insert into docs (docID, title, html) values (%s, %s, %s);'
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
	profStr = ''' 
http://www.cs.sfu.ca/people/faculty/gregbaker.html http://www.cs.sfu.ca/~ggbaker/ http://www.cs.sfu.ca/people/faculty/bradleybart.html http://www.cs.sfu.ca/~bbart/ http://www.cs.sfu.ca/people/faculty/petraberenbrink.html http://www.cs.sfu.ca/~petra/ http://www.cs.sfu.ca/people/faculty/binaybhattacharya.html http://www.cs.sfu.ca/~binay/ http://www.cs.sfu.ca/people/faculty/andreibulatov.html http://www.cs.sfu.ca/~abulatov/ http://www.cs.sfu.ca/people/faculty/robertdcameron.html http://www.cs.sfu.ca/~cameron/ http://www.cs.sfu.ca/people/faculty/dianacukierman.html http://www.cs.sfu.ca/people/faculty/ryandarcy.html http://www.cs.sfu.ca/%7Everonica/ http://www.cs.sfu.ca/people/faculty/veronicadahl1.html http://www.cs.sfu.ca/~veronica/ http://www.cs.sfu.ca/people/faculty/jamesdelgrande.html http://www.cs.sfu.ca/~jim/ http://www.cs.sfu.ca/people/faculty/tonydixon.html http://www.cs.sfu.ca/people/faculty/tobydonaldson.html http://www.cs.sfu.ca/people/faculty/markdrew.html http://www.cs.sfu.ca/~mark/ http://www.cs.sfu.ca/people/faculty/johnedgar.html http://www.cs.sfu.ca/people/faculty/fundaergun.html http://www.cs.sfu.ca/~funda/ http://www.cs.sfu.ca/people/faculty/martinester.html http://www.cs.sfu.ca/~ester/ http://www.cs.sfu.ca/people/faculty/mikeevans.html http://www.cs.sfu.ca/people/faculty/alexandrafedorova.html http://www.cs.sfu.ca/~fedorova/ http://www.cs.sfu.ca/people/faculty/brianfraser.html http://www.cs.sfu.ca/~bfraser/ http://www.cs.sfu.ca/people/faculty/brianfunt.html http://www.cs.sfu.ca/~funt/ http://www.cs.sfu.ca/people/faculty/uweglasser.html http://www.cs.sfu.ca/~glaesser/ http://www.cs.sfu.ca/people/faculty/QianpingGu.html http://www.cs.sfu.ca/~qgu/ http://www.cs.sfu.ca/people/faculty/louhafer.html http://www.cs.sfu.ca/~lou/ http://www.cs.sfu.ca/people/faculty/ghassanhamarneh.html http://www.cs.sfu.ca/~hamarneh/ http://www.cs.sfu.ca/people/faculty/mohamedhefeeda.html http://www.cs.sfu.ca/~mhefeeda/ http://www.cs.sfu.ca/people/faculty/pavolhell.html http://www.cs.sfu.ca/~pavol/ http://www.cs.sfu.ca/people/faculty/valentinekabanets.html http://www.cs.sfu.ca/~kabanets/ http://www.cs.sfu.ca/people/faculty/harindersinghkhangura.html http://www.cs.sfu.ca/~hskhangu/ http://www.cs.sfu.ca/people/faculty/arthurkirkpatrick.html http://www.cs.sfu.ca/~ted/ http://www.cs.sfu.ca/people/faculty/RameshKrishnamurti.html http://www.cs.sfu.ca/~ramesh/ http://www.cs.sfu.ca/people/faculty/annelavergne.html http://www.cs.sfu.ca/~alavergn/ http://www.cs.sfu.ca/people/faculty/ze-lianli.html http://www.cs.sfu.ca/~li/ http://www.cs.sfu.ca/people/faculty/arthurliestman.html http://www.cs.sfu.ca/~art/ http://www.cs.sfu.ca/people/faculty/jiangchuanliu.html http://www.cs.sfu.ca/~jcliu/ http://www.cs.sfu.ca/people/faculty/Wo-ShunLuk.html http://www.cs.sfu.ca/~woshun/ http://www.cs.sfu.ca/people/faculty/davidmitchell.html http://www.cs.sfu.ca/~mitchell/ http://www.cs.sfu.ca/people/faculty/gregmori.html http://www.cs.sfu.ca/~mori/ http://www.cs.sfu.ca/people/faculty/torstenmoller.html http://www.cs.sfu.ca/~torsten/ http://www.cs.sfu.ca/people/faculty/stevenpearce.html http://www.cs.sfu.ca/~stevenp/ http://www.cs.sfu.ca/people/faculty/jianpei.html http://www.cs.sfu.ca/~jpei/ http://www.cs.sfu.ca/people/faculty/JosephPeters.html http://www.cs.sfu.ca/~peters/ http://www.cs.sfu.ca/people/faculty/fredpopowich.html http://www.cs.sfu.ca/~popowich/ http://www.cs.sfu.ca/people/faculty/janiceregan.html http://www.cs.sfu.ca/~jregan/ http://www.cs.sfu.ca/people/faculty/cenkssahinalp.html http://www.cs.sfu.ca/~cenk/ http://www.cs.sfu.ca/people/faculty/anoopsarkar.html http://www.cs.sfu.ca/~anoop/ http://www.cs.sfu.ca/people/faculty/oliverschulte.html http://www.cs.sfu.ca/~oschulte/ http://www.cs.sfu.ca/people/faculty/thomasshermer.html http://www.cs.sfu.ca/~shermer/ http://www.cs.sfu.ca/people/Faculty/Profile/ashriram.html http://www.cs.sfu.ca/people/faculty/ArrvindhShriraman.html http://www.cs.sfu.ca/~ashriram/ http://www.cs.sfu.ca/people/Faculty/Profile/tamaras.html http://www.cs.sfu.ca/people/faculty/tamarasmyth.html http://www.cs.sfu.ca/~tamaras/ http://www.cs.sfu.ca/people/Faculty/Profile/tardos.html http://www.cs.sfu.ca/people/faculty/gabortardos.html http://www.cs.sfu.ca/~tardos/ http://www.cs.sfu.ca/people/Faculty/Profile/ter.html http://www.cs.sfu.ca/people/faculty/EugeniaTernovska.html http://www.cs.sfu.ca/~ter/ http://www.cs.sfu.ca/people/Faculty/Profile/vaughan.html http://www.cs.sfu.ca/people/faculty/richardvaughan.html http://www.cs.sfu.ca/~vaughan/ http://www.cs.sfu.ca/people/Faculty/Profile/wangk.html http://www.cs.sfu.ca/people/faculty/kewang.html http://www.cs.sfu.ca/~wangk/ http://www.cs.sfu.ca/people/faculty/kaywiese.html http://www.cs.sfu.ca/~wiese/ http://www.cs.sfu.ca/people/faculty/cynthiaxie.html http://www.cs.sfu.ca/people/Faculty/Profile/haoz.html http://www.cs.sfu.ca/people/faculty/richardzhang.html http://www.cs.sfu.ca/~haoz/'''
	seedURL = profStr.split(" ") 
	#seedURL = ['http://www.cs.sfu.ca/people/faculty.html','http://www.cs.sfu.ca/CourseCentral']
	parsedURL = []
	while len(seedURL)!=0:
##		if len(parsedURL)>20:
##			break;
		print '###### start iterate ######'
		url = seedURL.pop(0) #gets first element
		parsedURL.append(url)
		print 'Reading URL %s', url
		print 'Parsing seed URL'
		try:
			html = urllib2.urlopen(url)
		except:
			print 'can\'t open url'
			continue

		soup = BeautifulSoup(html)
		try:
		#	extractedLinks = extractInternalLinks(url, soup)
			pageTitle = clean(soup.title.string)
		except:
			print 'cannot clean page title, likely a PDF, skipping doc'
			continue

		docID = url
		docObj = doc(docID, pageTitle, html)

		try:
			sql = 'insert into docs (docID, title, html) values (%s, %s, %s);'
			cur.execute(sql, (docID, pageTitle, soup) )
		except:
			print 'duplicate entries'
		try:
			db.commit()
		except:
			print 'duplicates. check sql'
		parsedSet= Set(parsedURL)
		seedSet = Set(seedURL)
		#tempSet = Set(extractedLinks)

		#get all urls in tempSet that is not in parsedSet (tempSet - parsedSet)
		#toBeAddedURL = tempSet.difference(parsedSet)

		#seedSet = seedSet.union(toBeAddedURL)
		#seedURL = list(seedSet) #manually crawl seed URLs and end
		print 'length of seed URL ', len(seedURL)
		#print 'length of parsedURL ', len(list(tempSet))

		print '#####ending iteration####'

def extractInternalLinks(seedURL, parentSoup):
	links=[]

	for link in parentSoup.find_all('a'):
		link = link.get('href')
		try:
			link = urljoin(seedURL, link)
			if not('cs.sfu.ca' in link.lower()) or ('#' in link) or ('calendar' in link.lower()):
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
